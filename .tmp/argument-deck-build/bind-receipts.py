from pathlib import Path

from cli.artifacts import contract_for_path, validate_artifact
from cli.orchestrator import _visual_inspection_contract
from cli.run_manifest import build_dependency_fingerprint, update_artifact
from cli.strengthen import _visual_brief_contract


root = Path("/Users/christiankessleriv/Repos/ai-council-mwaa")
outputs = root / "outputs"
manifest = outputs / "run-manifest.json"
visual = outputs / "stage4/visual-brief.json"
deck = outputs / "stage4/argument-data-centers-on-aircraft-approach.pptx"
receipt = outputs / "stage4/argument-data-centers-on-aircraft-approach-visual-inspection.json"

visual_dependencies = (
    "run-manifest.json",
    "context/argument-request.md",
    "stage1/evidence-map.md",
    "evidence-ledger.jsonl",
    "claim-lineage.jsonl",
    "stage3/final-draft.md",
    "stage3/fact-check-report.md",
)
update_artifact(
    manifest,
    visual,
    validate_artifact(visual, _visual_brief_contract()),
    artifact_id="argument/visual-brief",
    producer="art-director",
    dependencies=build_dependency_fingerprint(manifest, visual_dependencies),
)

presentation_dependencies = (
    "run-manifest.json",
    "context/argument-request.md",
    "stage3/final-draft.md",
    "stage3/fact-check-report.md",
    "evidence-ledger.jsonl",
    "claim-lineage.jsonl",
    "stage4/visual-brief.json",
)
fingerprint = build_dependency_fingerprint(manifest, presentation_dependencies)
update_artifact(
    manifest,
    receipt,
    validate_artifact(receipt, _visual_inspection_contract()),
    producer="presentation-designer",
    dependencies=fingerprint,
)
update_artifact(
    manifest,
    deck,
    validate_artifact(deck, contract_for_path(deck)),
    artifact_id="argument/presentation",
    producer="presentation-designer",
    dependencies=fingerprint,
)

print("Bound visual brief, deck, and inspection receipt to current dependencies.")
