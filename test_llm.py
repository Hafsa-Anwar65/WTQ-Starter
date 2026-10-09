"""Run this TONIGHT: python test_llm.py  -> confirms your API key + model work."""
from llm import call_llm, call_llm_json, model_label

print("Using:", model_label())
print("Text test :", call_llm("Say hello in one short sentence."))
print("JSON test :", call_llm_json('Return {"status": "ok", "number": 42}'))
print("\nAll good. You're ready for tomorrow.")
