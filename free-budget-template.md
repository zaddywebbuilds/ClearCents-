---
layout: default
title: "Free Monthly Budget Template"
description: "A simple, printable monthly budget template. Track income, expenses, savings, and debt — free to use, no sign-up required."
permalink: /free-budget-template/
---

<header class="page-hero">
  <div class="container">
    <nav class="breadcrumb" aria-label="Breadcrumb">
      <a href="{{ '/' | relative_url }}">Home</a>
      <span aria-hidden="true">›</span>
      <span aria-current="page">Free Budget Template</span>
    </nav>
    <h1 class="page-hero-title">Free Monthly Budget Template</h1>
    <p class="page-hero-sub">A clean, simple budget that works on any income. Fill in the numbers, find where your money is going, and start keeping more of it.</p>
  </div>
</header>

<div class="container">
  <div class="budget-page">

    <div class="budget-intro">
      <p>No email required. No app to download. Just a straightforward monthly budget you can use right now. Print it, copy it to a spreadsheet, or fill it in on screen.</p>
      <div class="budget-actions">
        <button class="btn btn-gold" onclick="window.print()">Print this template</button>
        <a href="https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgVE2upms/copy" target="_blank" rel="noopener" class="btn btn-outline">Copy to Google Sheets</a>
      </div>
    </div>

    <div class="budget-template" id="budgetTemplate">

      <div class="budget-header">
        <h2>Monthly Budget</h2>
        <div class="budget-month">Month: _____________________ &nbsp;&nbsp; Year: _________</div>
      </div>

      <!-- INCOME -->
      <div class="budget-section">
        <div class="budget-section-title income-title">Income</div>
        <table class="budget-table">
          <thead>
            <tr><th>Source</th><th>Budgeted</th><th>Actual</th><th>Difference</th></tr>
          </thead>
          <tbody>
            <tr><td>Primary job (take-home)</td><td>$</td><td>$</td><td>$</td></tr>
            <tr><td>Side hustle / freelance</td><td>$</td><td>$</td><td>$</td></tr>
            <tr><td>Other income</td><td>$</td><td>$</td><td>$</td></tr>
            <tr class="total-row"><td><strong>Total Income</strong></td><td>$</td><td>$</td><td>$</td></tr>
          </tbody>
        </table>
      </div>

      <!-- FIXED EXPENSES -->
      <div class="budget-section">
        <div class="budget-section-title">Fixed Expenses</div>
        <table class="budget-table">
          <thead>
            <tr><th>Category</th><th>Budgeted</th><th>Actual</th><th>Difference</th></tr>
          </thead>
          <tbody>
            <tr><td>Rent / Mortgage</td><td>$</td><td>$</td><td>$</td></tr>
            <tr><td>Car payment</td><td>$</td><td>$</td><td>$</td></tr>
            <tr><td>Car insurance</td><td>$</td><td>$</td><td>$</td></tr>
            <tr><td>Health insurance</td><td>$</td><td>$</td><td>$</td></tr>
            <tr><td>Internet / phone</td><td>$</td><td>$</td><td>$</td></tr>
            <tr><td>Subscriptions</td><td>$</td><td>$</td><td>$</td></tr>
            <tr><td>Student loans</td><td>$</td><td>$</td><td>$</td></tr>
            <tr><td>Other fixed</td><td>$</td><td>$</td><td>$</td></tr>
            <tr class="total-row"><td><strong>Total Fixed</strong></td><td>$</td><td>$</td><td>$</td></tr>
          </tbody>
        </table>
      </div>

      <!-- VARIABLE EXPENSES -->
      <div class="budget-section">
        <div class="budget-section-title">Variable Expenses</div>
        <table class="budget-table">
          <thead>
            <tr><th>Category</th><th>Budgeted</th><th>Actual</th><th>Difference</th></tr>
          </thead>
          <tbody>
            <tr><td>Groceries</td><td>$</td><td>$</td><td>$</td></tr>
            <tr><td>Gas / transportation</td><td>$</td><td>$</td><td>$</td></tr>
            <tr><td>Utilities (electric, water, gas)</td><td>$</td><td>$</td><td>$</td></tr>
            <tr><td>Dining out / takeout</td><td>$</td><td>$</td><td>$</td></tr>
            <tr><td>Entertainment</td><td>$</td><td>$</td><td>$</td></tr>
            <tr><td>Clothing</td><td>$</td><td>$</td><td>$</td></tr>
            <tr><td>Personal care</td><td>$</td><td>$</td><td>$</td></tr>
            <tr><td>Medical / copays</td><td>$</td><td>$</td><td>$</td></tr>
            <tr><td>Household / home</td><td>$</td><td>$</td><td>$</td></tr>
            <tr><td>Kids / pet expenses</td><td>$</td><td>$</td><td>$</td></tr>
            <tr><td>Miscellaneous</td><td>$</td><td>$</td><td>$</td></tr>
            <tr class="total-row"><td><strong>Total Variable</strong></td><td>$</td><td>$</td><td>$</td></tr>
          </tbody>
        </table>
      </div>

      <!-- SAVINGS & DEBT -->
      <div class="budget-section">
        <div class="budget-section-title savings-title">Savings &amp; Debt Payoff</div>
        <table class="budget-table">
          <thead>
            <tr><th>Category</th><th>Budgeted</th><th>Actual</th><th>Difference</th></tr>
          </thead>
          <tbody>
            <tr><td>Emergency fund</td><td>$</td><td>$</td><td>$</td></tr>
            <tr><td>Retirement (401k / IRA)</td><td>$</td><td>$</td><td>$</td></tr>
            <tr><td>Extra debt payment</td><td>$</td><td>$</td><td>$</td></tr>
            <tr><td>Sinking funds / goals</td><td>$</td><td>$</td><td>$</td></tr>
            <tr class="total-row"><td><strong>Total Savings</strong></td><td>$</td><td>$</td><td>$</td></tr>
          </tbody>
        </table>
      </div>

      <!-- SUMMARY -->
      <div class="budget-summary">
        <div class="summary-row">
          <span>Total Income</span><span class="summary-val">$</span>
        </div>
        <div class="summary-row">
          <span>Total Expenses + Savings</span><span class="summary-val">$</span>
        </div>
        <div class="summary-row summary-balance">
          <span><strong>Remaining (should be $0)</strong></span><span class="summary-val">$</span>
        </div>
      </div>

      <p class="budget-tip"><strong>Zero-based budgeting tip:</strong> Give every dollar a job until your Remaining balance equals $0. If you have money left over, send it to savings or extra debt payments — don't let it disappear.</p>

    </div><!-- end .budget-template -->

    <div class="prose-page" style="padding-top: 1rem;">
      <h2>How to use this budget</h2>
      <p><strong>Step 1 — Fill in your income first.</strong> Use your take-home (after-tax) pay, not your gross salary. If your income varies, use your lowest expected month.</p>
      <p><strong>Step 2 — List your fixed expenses.</strong> These are the same every month — rent, car payment, subscriptions. Write what you plan to spend in "Budgeted," then fill in "Actual" at the end of the month.</p>
      <p><strong>Step 3 — Estimate variable expenses.</strong> Look at last month's bank statement for a realistic starting point. Most people underestimate groceries and dining by 30–40%.</p>
      <p><strong>Step 4 — Budget savings like a bill.</strong> Put savings and debt payoff before discretionary spending, not after. Pay yourself first.</p>
      <p><strong>Step 5 — Get to zero.</strong> Total income minus all expenses and savings should equal $0. Every dollar should have a job assigned before the month starts.</p>
    </div>

  </div>
</div>

<style>
.budget-page { padding: 2.5rem 0 5rem; max-width: 860px; margin: 0 auto; }
.budget-intro { margin-bottom: 2.5rem; color: var(--text-3); line-height: 1.7; }
.budget-intro p { margin-bottom: 1.25rem; }
.budget-actions { display: flex; gap: 1rem; flex-wrap: wrap; }
.budget-template {
  background: var(--bg-1);
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-lg);
  padding: 2rem 2.5rem;
  margin-bottom: 2rem;
}
.budget-header { margin-bottom: 1.75rem; border-bottom: 2px solid var(--gold); padding-bottom: 1rem; }
.budget-header h2 { font-size: 1.6rem; font-weight: 700; color: var(--gold); margin: 0 0 0.5rem; }
.budget-month { font-size: 0.9rem; color: var(--text-3); }
.budget-section { margin-bottom: 2rem; }
.budget-section-title {
  font-size: 0.78rem; font-weight: 700; text-transform: uppercase;
  letter-spacing: 0.08em; color: var(--text-4);
  border-left: 3px solid var(--glass-border);
  padding-left: 0.75rem; margin-bottom: 0.75rem;
}
.income-title { border-color: var(--green); color: var(--green); }
.savings-title { border-color: var(--gold); color: var(--gold); }
.budget-table { width: 100%; border-collapse: collapse; font-size: 0.9rem; }
.budget-table th {
  text-align: left; font-size: 0.72rem; font-weight: 600;
  text-transform: uppercase; letter-spacing: 0.05em;
  color: var(--text-4); padding: 0.4rem 0.6rem;
  border-bottom: 1px solid var(--glass-border);
}
.budget-table td {
  padding: 0.55rem 0.6rem;
  border-bottom: 1px solid rgba(255,255,255,0.04);
  color: var(--text-2);
}
.budget-table td:not(:first-child) { color: var(--text-4); width: 15%; }
.total-row td { font-weight: 700; color: var(--text-1) !important; border-top: 1px solid var(--glass-border); }
.budget-summary {
  background: var(--bg-2); border-radius: var(--radius);
  padding: 1.25rem 1.5rem; margin-top: 1.5rem;
}
.summary-row {
  display: flex; justify-content: space-between; align-items: center;
  padding: 0.5rem 0; border-bottom: 1px solid var(--glass-border);
  color: var(--text-2); font-size: 0.95rem;
}
.summary-row:last-child { border-bottom: none; }
.summary-balance { color: var(--gold) !important; }
.summary-val { font-family: var(--font-heading); font-weight: 700; min-width: 80px; text-align: right; }
.budget-tip {
  margin-top: 1.5rem; padding: 1rem 1.25rem;
  background: rgba(0,208,132,0.06);
  border: 1px solid rgba(0,208,132,0.15);
  border-radius: var(--radius);
  font-size: 0.88rem; color: var(--text-3); line-height: 1.65;
}

@media print {
  .site-header, .site-footer, .budget-actions, .page-hero, nav, .prose-page { display: none !important; }
  .budget-template { border: 1px solid #ccc; background: white; color: black; padding: 1rem; }
  .budget-table td, .budget-table th { color: black !important; border-color: #ccc; }
  .budget-section-title { color: #333 !important; border-color: #999; }
  .budget-header h2 { color: #000; }
  body { background: white; }
}
@media (max-width: 600px) {
  .budget-template { padding: 1.25rem; }
  .budget-table { font-size: 0.78rem; }
  .budget-table td:nth-child(3), .budget-table th:nth-child(3),
  .budget-table td:nth-child(4), .budget-table th:nth-child(4) { display: none; }
}
</style>
