"""ZKP age verification stub with clear production interface."""

import hashlib
import secrets
from datetime import datetime, timezone

from nexus_common.domain.enums import VerificationStatus
from nexus_common.domain.models import ZKPAgeProof, ZKPVerificationResult


class ZKPVerifier:
    """
    Stub ZKP verifier for development.
    Production: replace with audited zk library (e.g., Semaphore, iden3, partner API).
    """

    STUB_VALID_PREFIX = "zkp_valid_"

    def verify_age(self, proof: ZKPAgeProof) -> ZKPVerificationResult:
        proof_hash = hashlib.sha256(proof.proof.encode()).hexdigest()[:16]

        # Stub: proofs starting with zkp_valid_ pass; empty proofs fail
        if proof.proof.startswith(self.STUB_VALID_PREFIX):
            return ZKPVerificationResult(
                verified=True,
                status=VerificationStatus.VERIFIED,
                minimum_age_met=True,
                message=f"Age verification passed (stub, min age {proof.minimum_age})",
                proof_hash=proof_hash,
            )

        if proof.proof == "demo_adult":
            return ZKPVerificationResult(
                verified=True,
                status=VerificationStatus.VERIFIED,
                minimum_age_met=True,
                message="Demo adult verification passed",
                proof_hash=proof_hash,
            )

        if proof.proof == "demo_minor":
            return ZKPVerificationResult(
                verified=False,
                status=VerificationStatus.FAILED,
                minimum_age_met=False,
                message="Age requirement not met",
                proof_hash=proof_hash,
            )

        return ZKPVerificationResult(
            verified=False,
            status=VerificationStatus.FAILED,
            minimum_age_met=False,
            message="Invalid or unverifiable ZKP proof",
            proof_hash=proof_hash,
        )

    def generate_stub_proof(self, is_adult: bool = True, minimum_age: int = 18) -> ZKPAgeProof:
        """Generate a stub proof for testing/demo flows."""
        token = secrets.token_hex(8)
        prefix = self.STUB_VALID_PREFIX if is_adult else "zkp_invalid_"
        return ZKPAgeProof(
            proof=f"{prefix}{token}",
            public_inputs={"min_age": str(minimum_age), "issued": datetime.now(timezone.utc).isoformat()},
            minimum_age=minimum_age,
        )