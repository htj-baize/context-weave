from context_weave.registry import REGISTRY


def test_registry_contains_first_context_family() -> None:
    assert "context.build" in REGISTRY
    assert "context.trace" in REGISTRY
    assert "target.build" in REGISTRY
    assert "target.bind" in REGISTRY
    assert "operate.validate" in REGISTRY
    assert "operate.prepare" in REGISTRY
    assert "operate.route" in REGISTRY


def test_registry_entries_have_product_metadata() -> None:
    entry = REGISTRY["context.build"]
    assert entry["description"]
    assert entry["when_to_use"]
    assert entry["expected_outputs"]
    assert entry["skill_doc"].endswith("SKILL.md")
