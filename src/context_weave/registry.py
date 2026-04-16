from __future__ import annotations

from context_weave.context.build import build_context
from context_weave.context.merge import merge_contexts
from context_weave.context.read import read_context
from context_weave.context.slice import slice_context
from context_weave.context.snapshot import snapshot_context
from context_weave.context.trace import trace_context
from context_weave.skill_catalog import skill_doc_path
from context_weave.operate.prepare import prepare_operation
from context_weave.operate.route import route_operation
from context_weave.operate.validate import validate_operation
from context_weave.target.bind import bind_target
from context_weave.target.build import build_target
from context_weave.target.read import read_target


REGISTRY = {
    "context.read": {
        "summary": "Read an existing standard context asset.",
        "description": "Read an existing standard context asset from a known reference.",
        "when_to_use": ["A workflow already has a context ref or snapshot file."],
        "when_not_to_use": ["The workflow still needs to build a context from source state."],
        "args": ["context_ref"],
        "expected_outputs": ["context", "context_metadata"],
        "side_effects": "none",
        "skill_doc": skill_doc_path("cw-context"),
        "callable": read_context,
    },
    "context.build": {
        "summary": "Build a standard context from a source state.",
        "description": "Build a standard context from a declared source state.",
        "when_to_use": ["The workflow only has raw source state and needs a standard context."],
        "when_not_to_use": ["A valid standard context already exists."],
        "args": ["source_kind", "source_ref", "build_profile"],
        "expected_outputs": ["context", "build_summary"],
        "side_effects": "none",
        "skill_doc": skill_doc_path("cw-context"),
        "callable": build_context,
    },
    "context.merge": {
        "summary": "Merge multiple contexts into a single context.",
        "description": "Merge multiple contexts into a single context using a declared merge policy.",
        "when_to_use": ["A task depends on more than one context source."],
        "when_not_to_use": ["A single context already fully represents the task."],
        "args": ["contexts", "merge_policy"],
        "expected_outputs": ["context", "merge_summary"],
        "side_effects": "none",
        "skill_doc": skill_doc_path("cw-context"),
        "callable": merge_contexts,
    },
    "context.slice": {
        "summary": "Slice a task-specific sub-context from a full context.",
        "description": "Slice a task-specific sub-context from a larger context.",
        "when_to_use": ["A downstream operation should consume a narrower task-specific context."],
        "when_not_to_use": ["The downstream operation intentionally needs the full context."],
        "args": ["context", "slice_profile"],
        "expected_outputs": ["context", "slice_summary"],
        "side_effects": "none",
        "skill_doc": skill_doc_path("cw-context"),
        "callable": slice_context,
    },
    "context.snapshot": {
        "summary": "Persist a context as a recoverable snapshot.",
        "description": "Persist a context as a recoverable snapshot artifact.",
        "when_to_use": ["A workflow needs resume, review, replay, or debug support."],
        "when_not_to_use": ["The context is purely transient and in-memory."],
        "args": ["context", "output_path", "label"],
        "expected_outputs": ["snapshot_ref", "snapshot_metadata"],
        "side_effects": "writes snapshot artifact",
        "skill_doc": skill_doc_path("cw-context"),
        "callable": snapshot_context,
    },
    "context.trace": {
        "summary": "Read lineage and provenance information from a context.",
        "description": "Read lineage and provenance information from a context.",
        "when_to_use": ["A workflow needs explainability or lineage inspection."],
        "when_not_to_use": ["Only the current payload matters and lineage is irrelevant."],
        "args": ["context"],
        "expected_outputs": ["trace", "lineage_summary"],
        "side_effects": "none",
        "skill_doc": skill_doc_path("cw-context"),
        "callable": trace_context,
    },
    "target.read": {
        "summary": "Read an existing standard target asset.",
        "description": "Read an existing standard target asset from a known reference.",
        "when_to_use": ["A workflow already has a target descriptor or wrapper file."],
        "when_not_to_use": ["The workflow still needs to define the target schema surface."],
        "args": ["target_ref"],
        "expected_outputs": ["target", "target_metadata"],
        "side_effects": "none",
        "skill_doc": skill_doc_path("cw-target"),
        "callable": read_target,
    },
    "target.build": {
        "summary": "Build a standard target descriptor from schema-facing inputs.",
        "description": "Build a standard target descriptor from schema reference and declared input requirements.",
        "when_to_use": ["A workflow needs a formal target surface before downstream validation or apply steps."],
        "when_not_to_use": ["A stable target descriptor already exists and can be read directly."],
        "args": ["schema_ref", "required_inputs", "optional_inputs", "constraints"],
        "expected_outputs": ["target", "build_summary"],
        "side_effects": "none",
        "skill_doc": skill_doc_path("cw-target"),
        "callable": build_target,
    },
    "target.bind": {
        "summary": "Project a context onto a declared target surface.",
        "description": "Validate required inputs and project a context payload onto a declared target surface.",
        "when_to_use": ["A workflow has both context and target and needs a target-specific input view."],
        "when_not_to_use": ["The workflow still needs context lifecycle work or target definition work."],
        "args": ["context", "target"],
        "expected_outputs": ["binding", "binding_summary"],
        "side_effects": "none",
        "skill_doc": skill_doc_path("cw-target"),
        "callable": bind_target,
    },
    "operate.validate": {
        "summary": "Validate whether a target binding is ready for downstream operation.",
        "description": "Validate a target binding and return a stable readiness report.",
        "when_to_use": ["A workflow needs a stable readiness check before preparing or routing an operation."],
        "when_not_to_use": ["The workflow still lacks a binding or still needs target binding work."],
        "args": ["binding"],
        "expected_outputs": ["report", "validation_summary"],
        "side_effects": "none",
        "skill_doc": skill_doc_path("cw-operate"),
        "callable": validate_operation,
    },
    "operate.prepare": {
        "summary": "Prepare a structured operation request from a ready target binding.",
        "description": "Prepare a neutral operation request payload from a ready target binding without executing it.",
        "when_to_use": ["A workflow has a ready binding and needs a stable request envelope for downstream execution."],
        "when_not_to_use": ["The binding still has missing required inputs or execution should happen directly here."],
        "args": ["binding", "operation_kind"],
        "expected_outputs": ["request", "request_summary"],
        "side_effects": "none",
        "skill_doc": skill_doc_path("cw-operate"),
        "callable": prepare_operation,
    },
    "operate.route": {
        "summary": "Route a target binding to the next appropriate skill step.",
        "description": "Route a target binding to a stable next step based on current readiness.",
        "when_to_use": ["A workflow needs deterministic next-step routing after binding."],
        "when_not_to_use": ["The workflow already knows the exact next step or needs custom orchestration logic."],
        "args": ["binding"],
        "expected_outputs": ["decision", "route_summary"],
        "side_effects": "none",
        "skill_doc": skill_doc_path("cw-operate"),
        "callable": route_operation,
    },
}
