"""День 18. Evals для агента: сценарии с ожидаемым поведением."""


def run_scenarios(scenarios, agent):
    """Прогнать агента по сценариям. agent(input) -> {"answer": str, "steps": [{"tool": ...}, ...]}.
    Сценарий: {"name", "input", и необязательные проверки:
      "expect_tools": [...]      все эти инструменты должны быть вызваны,
      "forbid_tools": [...]      ни один из этих не должен быть вызван,
      "expect_in_answer": [...]  каждая подстрока есть в ответе (без учёта регистра),
      "max_steps": n}            шагов не больше n.
    Агент упал -> сценарий провален с причиной, остальные продолжают выполняться.
    Вернуть {"total", "passed", "results": [{"name", "passed": bool, "reasons": [строки]}]}.
    У пройденного сценария reasons пустой; у проваленного по строке на каждую нарушенную проверку.
    """
    results = []
    for sc in scenarios:
        reasons = []
        try:
            out = agent(sc["input"])
            used = [s["tool"] for s in out.get("steps", [])]
            answer = (out.get("answer") or "").lower()
            for t in sc.get("expect_tools", []):
                if t not in used:
                    reasons.append(f"не вызван инструмент {t}")
            for t in sc.get("forbid_tools", []):
                if t in used:
                    reasons.append(f"вызван запрещённый инструмент {t}")
            for s in sc.get("expect_in_answer", []):
                if s.lower() not in answer:
                    reasons.append(f"в ответе нет {s!r}")
            if "max_steps" in sc and len(used) > sc["max_steps"]:
                reasons.append(f"шагов {len(used)}, лимит {sc['max_steps']}")
        except Exception as e:  # noqa: BLE001
            reasons.append(f"агент упал: {e}")
        results.append({"name": sc["name"], "passed": not reasons, "reasons": reasons})
    return {"total": len(results), "passed": sum(r["passed"] for r in results), "results": results}
