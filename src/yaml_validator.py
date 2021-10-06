"""Use me as a standalone module to check the contents of quote_library.yaml

This module loads and prints the contents of said YAML file,
so that developers can catch any nasty encoding/syntax issues.
To use this as a standalone module, try doing the following in PowerShell:
python yaml_validator.py *> yaml_contents.txt
"""
import yaml_parser


FILE_TO_CHECK = "quote_library.yaml"
QUOTE_LIBRARY = yaml_parser.yaml_load(FILE_TO_CHECK)


print("*** Standalone Module - YAML Validator ***")
print(f"\nNow attempting to catch any non-ASCII quotes in {FILE_TO_CHECK}...")
for person in QUOTE_LIBRARY.values():
	for quote in person.get("quotes"):
		if not quote.isascii():
			print(f"  Found non-ASCII by {person}:\n  {quote}")


print("\nCatch sequence completed!")
# print("-----------------------------------")
# print(f"\nAppendix - data parsed from {FILE_TO_CHECK}:\n")
# print(QUOTE_LIBRARY)
