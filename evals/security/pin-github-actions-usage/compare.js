#!/usr/bin/env node

import { readFileSync, readdirSync, existsSync, statSync } from "fs";
import { join, resolve } from "path";

const DEFAULT_RESULTS_DIR = "vally-experiment-results";
const PRIMARY_VARIANTS = ["scripted-main", "skill-only-baseline"];

function fail(message) {
  console.error(message);
  process.exit(1);
}

function readJsonLines(filePath) {
  return readFileSync(filePath, "utf8")
    .split("\n")
    .map((line) => line.trim())
    .filter(Boolean)
    .map((line) => JSON.parse(line));
}

function latestRunDir(resultsRoot) {
  const entries = readdirSync(resultsRoot, { withFileTypes: true })
    .filter((entry) => entry.isDirectory())
    .map((entry) => entry.name)
    .sort();

  if (entries.length === 0) {
    fail(`No experiment runs found in ${resultsRoot}`);
  }

  return join(resultsRoot, entries[entries.length - 1]);
}

function resolveRunDir(argPath) {
  const candidate = argPath || DEFAULT_RESULTS_DIR;
  const resolved = resolve(candidate);

  if (!existsSync(resolved)) {
    fail(`Experiment output path not found: ${candidate}`);
  }

  if (!statSync(resolved).isDirectory()) {
    fail(`Experiment output path is not a directory: ${candidate}`);
  }

  if (existsSync(join(resolved, "report.md"))) {
    return resolved;
  }

  return latestRunDir(resolved);
}

function collectVariantMetrics(runDir, variant) {
  const resultsPath = join(runDir, variant, "results.jsonl");
  if (!existsSync(resultsPath)) {
    fail(`Missing results for variant '${variant}' in ${runDir}`);
  }

  const trials = readJsonLines(resultsPath).filter((row) => row.type === "trial-result");
  if (trials.length === 0) {
    fail(`No trial results found for variant '${variant}' in ${resultsPath}`);
  }

  const totals = {
    totalTokens: 0,
    inputTokens: 0,
    outputTokens: 0,
    modelCalls: 0,
    usdCost: 0,
  };
  let hasUsdCost = false;

  for (const trial of trials) {
    const metrics = trial.trajectory?.metrics || {};
    const tokenUsage = metrics.tokenUsage || {};

    totals.totalTokens += tokenUsage.totalTokens || 0;
    totals.inputTokens += tokenUsage.inputTokens || 0;
    totals.outputTokens += tokenUsage.outputTokens || 0;
    totals.modelCalls += tokenUsage.callCount || 0;

    const explicitCost = metrics.costUsd ?? tokenUsage.costUsd ?? trial.costUsd;
    if (typeof explicitCost === "number") {
      totals.usdCost += explicitCost;
      hasUsdCost = true;
    }
  }

  return { trials: trials.length, totals, hasUsdCost };
}

function formatNumber(value) {
  if (typeof value !== "number" || Number.isNaN(value)) {
    return "—";
  }

  return new Intl.NumberFormat("en-US").format(value);
}

function formatPercent(value) {
  if (!Number.isFinite(value)) {
    return "—";
  }

  const sign = value > 0 ? "+" : value < 0 ? "-" : "";
  return `${sign}${Math.abs(value).toFixed(2)}%`;
}

function formatDelta(delta, baseline) {
  if (!Number.isFinite(delta) || !Number.isFinite(baseline) || baseline === 0) {
    return "—";
  }

  return formatPercent((delta / baseline) * 100);
}

function compareMetric(scripted, baseline, key) {
  const delta = scripted.totals[key] - baseline.totals[key];
  return {
    scripted: scripted.totals[key],
    baseline: baseline.totals[key],
    relative: formatDelta(delta, baseline.totals[key]),
  };
}

function metricRows(scripted, baseline) {
  const rows = [
    ["Total tokens", compareMetric(scripted, baseline, "totalTokens")],
    ["Input tokens", compareMetric(scripted, baseline, "inputTokens")],
    ["Output tokens", compareMetric(scripted, baseline, "outputTokens")],
    ["Model calls", compareMetric(scripted, baseline, "modelCalls")],
  ];

  if (scripted.hasUsdCost || baseline.hasUsdCost) {
    rows.unshift(["USD cost", compareMetric(scripted, baseline, "usdCost")]);
  }

  return rows;
}

function printMarkdownTable(runDir, scripted, baseline) {
  console.log(`Run: ${runDir}`);
  console.log("");
  console.log(`Trials per variant: ${scripted.trials}`);
  console.log("");
  console.log(`| Metric across ${scripted.trials} trials | Scripted | Skill-only baseline | Delta (scripted vs baseline) |`);
  console.log("| --- | --- | --- | --- |");

  for (const [label, values] of metricRows(scripted, baseline)) {
    console.log(
      `| ${label} | ${formatNumber(values.scripted)} | ${formatNumber(values.baseline)} | ${values.relative} |`
    );
  }
}

function main() {
  const runDir = resolveRunDir(process.argv[2]);
  const variants = readdirSync(runDir, { withFileTypes: true })
    .filter((entry) => entry.isDirectory())
    .map((entry) => entry.name);

  for (const variant of PRIMARY_VARIANTS) {
    if (!variants.includes(variant)) {
      fail(`Expected variant '${variant}' in ${runDir}. Found variants: ${variants.sort().join(", ")}`);
    }
  }

  const scripted = collectVariantMetrics(runDir, "scripted-main");
  const baseline = collectVariantMetrics(runDir, "skill-only-baseline");
  printMarkdownTable(runDir, scripted, baseline);
}

main();
