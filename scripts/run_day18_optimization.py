"""
Day 18 - Optimization & Performance Testing

Tests:
- Text extraction speed
- Cached extraction
- Noisy resume handling
- Entity detection
- Existing ATS pipeline vs optimized pipeline
- Stability across Day 17 test cases
"""

import json
import time
from pathlib import Path

from src.ats_pipeline.pipeline import ATSPipeline
from src.ats_optimization.optimizer import (
    fast_text_extraction,
    clean_noisy_resume,
    detect_entities,
    clear_cache,
    get_cache_info,
    calculate_improvement,
)
from src.ats_optimization.optimized_pipeline import OptimizedATSPipeline


BASE_DIR = Path(__file__).resolve().parent

RESUME_DIR = BASE_DIR / "data" / "day17_testing" / "resumes"
JD_DIR = BASE_DIR / "data" / "day17_testing" / "job_descriptions"

OUTPUT_DIR = BASE_DIR / "outputs" / "day18"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


TEST_CASES = [
    {
        "case_id": "TF001",
        "resume": RESUME_DIR / "technical_fresher.txt",
        "job": JD_DIR / "data_analyst.txt",
    },
    {
        "case_id": "TS001",
        "resume": RESUME_DIR / "technical_senior.txt",
        "job": JD_DIR / "senior_data_analyst.txt",
    },
    {
        "case_id": "NF001",
        "resume": RESUME_DIR / "nontechnical_fresher.txt",
        "job": JD_DIR / "business_analyst.txt",
    },
    {
        "case_id": "NS001",
        "resume": RESUME_DIR / "nontechnical_senior.txt",
        "job": JD_DIR / "senior_business_analyst.txt",
    },
]


def measure(function, *args):
    start = time.perf_counter()

    result = function(*args)

    elapsed = time.perf_counter() - start

    return result, elapsed


def main():

    print()
    print("=" * 65)
    print("DAY 18 - OPTIMIZATION & PERFORMANCE TESTING")
    print("=" * 65)
    print()

    # --------------------------------------------------------
    # TEXT EXTRACTION BENCHMARK
    # --------------------------------------------------------

    print("TEXT EXTRACTION PERFORMANCE")
    print("-" * 65)

    sample_resume = TEST_CASES[0]["resume"]

    # Baseline direct reading
    start = time.perf_counter()

    with open(
        sample_resume,
        "r",
        encoding="utf-8",
        errors="ignore"
    ) as file:
        baseline_text = file.read()

    baseline_time = time.perf_counter() - start

    # Optimized extraction first run
    clear_cache()

    _, optimized_first_time = measure(
        fast_text_extraction,
        str(sample_resume)
    )

    # Optimized cached run
    _, optimized_cached_time = measure(
        fast_text_extraction,
        str(sample_resume)
    )

    improvement_first = calculate_improvement(
        baseline_time,
        optimized_first_time
    )

    improvement_cached = calculate_improvement(
        baseline_time,
        optimized_cached_time
    )

    print(f"Baseline extraction : {baseline_time:.6f} sec")
    print(f"Optimized extraction: {optimized_first_time:.6f} sec")
    print(f"Cached extraction   : {optimized_cached_time:.6f} sec")
    print(f"First-run improvement: {improvement_first}%")
    print(f"Cached improvement   : {improvement_cached}%")

    cache_info = get_cache_info()

    print()
    print("CACHE INFORMATION")
    print("-" * 65)
    print(cache_info)

    # --------------------------------------------------------
    # NOISY RESUME TEST
    # --------------------------------------------------------

    print()
    print("NOISY RESUME HANDLING")
    print("-" * 65)

    noisy_resume = """
    ARUN   KUMAR
    Python   SQL   Excel   Pandas
    • • • DATA ANALYST • • •
    Email: arun@example.com
    Experience: 2   years
    """

    cleaned_resume = clean_noisy_resume(noisy_resume)
    entities = detect_entities(cleaned_resume)

    print("Original noisy text:")
    print(noisy_resume)

    print("Cleaned text:")
    print(cleaned_resume)

    print("Detected entities:")
    print(entities)

    # --------------------------------------------------------
    # FULL ATS PERFORMANCE TEST
    # --------------------------------------------------------

    print()
    print("FULL ATS PERFORMANCE")
    print("-" * 65)

    baseline_pipeline = ATSPipeline()
    optimized_pipeline = OptimizedATSPipeline()

    results = []

    for case in TEST_CASES:

        print()
        print(f"CASE: {case['case_id']}")

        # Baseline
        _, baseline_time = measure(
            baseline_pipeline.process_candidate,
            str(case["resume"]),
            str(case["job"]),
            case["case_id"],
        )

        # Optimized
        optimized_result, optimized_time = measure(
            optimized_pipeline.process_candidate,
            str(case["resume"]),
            str(case["job"]),
            case["case_id"],
        )

        improvement = calculate_improvement(
            baseline_time,
            optimized_time
        )

        print(f"Baseline time : {baseline_time:.6f} sec")
        print(f"Optimized time: {optimized_time:.6f} sec")
        print(f"Improvement   : {improvement}%")
        print(f"ATS score     : {optimized_result['ats_score']}")
        print(f"Classification: {optimized_result['classification']}")

        results.append({
            "case_id": case["case_id"],
            "baseline_time_seconds": round(baseline_time, 6),
            "optimized_time_seconds": round(optimized_time, 6),
            "improvement_percent": improvement,
            "ats_score": optimized_result["ats_score"],
            "classification": optimized_result["classification"],
            "entities": optimized_result["analysis"].get(
                "entities",
                {}
            ),
        })

    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    total_baseline = sum(
        item["baseline_time_seconds"]
        for item in results
    )

    total_optimized = sum(
        item["optimized_time_seconds"]
        for item in results
    )

    overall_improvement = calculate_improvement(
        total_baseline,
        total_optimized
    )

    report = {
        "day": 18,
        "title": "ATS Optimization & Performance Tuning",
        "objective": "Make ATS production-ready",
        "optimizations": [
            "Cached text extraction",
            "Noisy resume normalization",
            "Lightweight entity detection",
            "Memory-friendly batch processing",
            "Reuse of existing ATS pipeline components",
        ],
        "text_extraction": {
            "baseline_seconds": round(baseline_time, 6),
            "optimized_first_run_seconds": round(
                optimized_first_time,
                6
            ),
            "optimized_cached_seconds": round(
                optimized_cached_time,
                6
            ),
            "first_run_improvement_percent": improvement_first,
            "cached_improvement_percent": improvement_cached,
        },
        "cache": cache_info,
        "ats_performance": {
            "total_baseline_seconds": round(
                total_baseline,
                6
            ),
            "total_optimized_seconds": round(
                total_optimized,
                6
            ),
            "overall_improvement_percent": overall_improvement,
            "cases_tested": len(results),
        },
        "cases": results,
        "stability": {
            "all_cases_completed": len(results) == len(TEST_CASES),
            "no_runtime_error": True,
        },
        "improvement_backlog": [
            {
                "id": "IB18-01",
                "item": "Further optimize PDF extraction",
                "priority": "Medium",
            },
            {
                "id": "IB18-02",
                "item": "Benchmark larger resume batches",
                "priority": "Medium",
            },
            {
                "id": "IB18-03",
                "item": "Profile memory usage with production-scale data",
                "priority": "Low",
            },
        ],
    }

    report_path = OUTPUT_DIR / "day18_performance_report.json"

    with open(
        report_path,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            report,
            file,
            indent=4
        )

    print()
    print("=" * 65)
    print("DAY 18 SUMMARY")
    print("=" * 65)
    print(f"Cases tested       : {len(results)}")
    print(f"Baseline total     : {total_baseline:.6f} sec")
    print(f"Optimized total    : {total_optimized:.6f} sec")
    print(f"Overall improvement: {overall_improvement}%")
    print()
    print("Performance report:")
    print(report_path)
    print()


if __name__ == "__main__":
    main()
