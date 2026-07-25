// ClearCents — Email Lead Collector
// Deploy this as a Google Apps Script Web App.
// Emails from your blog subscribe form land in the linked Google Sheet.
//
// HOW TO DEPLOY:
// 1. Go to https://script.google.com → New project
// 2. Paste this entire file in, replacing any existing code
// 3. Click the floppy disk (Save), name it "ClearCents Leads"
// 4. Click Deploy → New deployment → Web app
//    - Execute as: Me
//    - Who has access: Anyone
// 5. Click Deploy → copy the Web App URL
// 6. In clearcents/assets/js/main.js, replace PASTE_YOUR_APPS_SCRIPT_URL_HERE with that URL
// 7. Commit and push — done. Emails now log to your Google Sheet.

var SHEET_NAME = 'Leads';

function doGet(e) {
  var email = (e.parameter.email || '').trim().toLowerCase();

  if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    return ContentService
      .createTextOutput(JSON.stringify({ status: 'error', message: 'Invalid email' }))
      .setMimeType(ContentService.MimeType.JSON);
  }

  var ss    = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName(SHEET_NAME) || ss.insertSheet(SHEET_NAME);

  // Add header row if sheet is empty
  if (sheet.getLastRow() === 0) {
    sheet.appendRow(['Email', 'Date', 'Source']);
    sheet.getRange(1, 1, 1, 3).setFontWeight('bold');
  }

  // Check for duplicates
  var existing = sheet.getRange(2, 1, Math.max(sheet.getLastRow() - 1, 1), 1).getValues();
  for (var i = 0; i < existing.length; i++) {
    if (existing[i][0] === email) {
      return ContentService
        .createTextOutput(JSON.stringify({ status: 'duplicate' }))
        .setMimeType(ContentService.MimeType.JSON);
    }
  }

  sheet.appendRow([email, new Date().toISOString(), 'ClearCents Blog']);

  return ContentService
    .createTextOutput(JSON.stringify({ status: 'ok' }))
    .setMimeType(ContentService.MimeType.JSON);
}
