# vcf2ics
Python project to convert vcf contacts to an ics calendar file, which contains the **birthdays** of the contacts

Purpose of the application:
Display birthdays in the Android calendar.  
It reads the `BDAY` tag from a vcf contacts file, writes the birthdays together with the calculated age into an ics calendar file.

This project was inspired by https://github.com/FoxP/VCF-to-ICS  
In comparison, the code has been simplified for the intended purpose.

Usage:
1. About the format of the vcf: it comes from the KDE/Plasma address management.
2. All entries that have a "BDAY" are processed, all others are ignored.
3. .ics is written (including with a calendar name)
4. with an additional app like "DAVx" you can upload this .ics to a CalDAV provider (e.g. mail.de) and integrate it into the Android calendar.
