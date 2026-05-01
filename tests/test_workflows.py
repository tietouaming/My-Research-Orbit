from research_orbit.workflows import list_workflows, load_workflow, render_system_prompt


def test_load_required_workflow() -> None:
    spec = load_workflow("research_memory_compactor")
    assert spec.name == "research_memory_compactor"
    assert spec.steps
    assert spec.safety_rules


def test_all_workflows_are_valid() -> None:
    specs = list_workflows()
    assert len(specs) >= 6
    assert {spec.name for spec in specs} >= {
        "research_memory_compactor",
        "word_mathtype_editor",
        "comsol_model_auditor",
        "simulation_porting_reviewer",
        "run_log_diagnoser",
        "application_pack_writer",
    }


def test_render_system_prompt_mentions_workflow() -> None:
    spec = load_workflow("run_log_diagnoser")
    prompt = render_system_prompt(spec)
    assert "run_log_diagnoser" in prompt
    assert "evidence" in prompt.lower()
