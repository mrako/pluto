import hashlib
import logging as log
import hmac


def validate_github_request_sha256(github_signature, webhook_secret, message) -> bool:
    if not webhook_secret:
        log.error("Github webhook_secret not defined! - Payload validation failed")
        return False

    github_signature = github_signature.strip()
    if not github_signature:
        log.error("No github signature")
        return False
    key = bytes(webhook_secret, 'UTF-8')
    hexdigest = hmac.new(key, message, hashlib.sha256).hexdigest()
    signature = "sha256=" + hexdigest
    result = github_signature == signature
    if not result:
        log.warning("Could not verify request signature! ({} vs. {})".format(github_signature, signature))
    return result
