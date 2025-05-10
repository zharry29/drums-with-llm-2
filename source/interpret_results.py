import argparse
import json
import os
import glob

# Argument parsing
parser = argparse.ArgumentParser(description="")
parser.add_argument('--data', choices=['instantiated', 'unrolled'], required=True, help="")
parser.add_argument('--model', default="gpt-4.1-mini", help="")
args = parser.parse_args()

results_dir = f"../outputs/{args.data}/{args.model}/test_results/"

def aggregate_results(results_dir):
    results = []
    for path in glob.glob(os.path.join(results_dir, "*.txt")):
        fn = os.path.basename(path)
        file_id = os.path.splitext(fn)[0]
        text = open(path).read()
        passed_universal_tests = not "Universal checks failed." in text
        actually_edited = not "No differences found." in text
        passed_unit_tests = "All unit tests passed." in text
        results.append({
            "file": file_id,
            "well_formed": passed_universal_tests,
            "actually_edited": actually_edited,
            "passed_unit_tests": passed_unit_tests
        })
        # Sort results by integer value of file_id
        results.sort(key=lambda r: int(r["file"]))
    passed_universal_tests_count = sum(r["well_formed"] for r in results)
    actually_edited_count = sum(r["actually_edited"] for r in results if r["well_formed"])
    passed_unit_tests_count = sum(r["passed_unit_tests"] for r in results if r["actually_edited"])
    report = {
        "well_formed": passed_universal_tests_count,
        "actually_edited": actually_edited_count,
        "passed_unit_tests": passed_unit_tests_count,
        "results": results
    }
    out = os.path.join(f"../outputs/{args.data}/{args.model}", "report.json")
    with open(out, "w") as f:
        json.dump(report, f, indent=2)
    print(f"Written report → {out}")

if __name__ == "__main__":
    aggregate_results(results_dir)
