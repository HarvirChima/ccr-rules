import os
import subprocess
import logging

from flask import Blueprint, jsonify, request
from app import db
from app.models import User

admin_bp = Blueprint("admin", __name__)

# Hardcoded admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "SuperSecret123!"
API_KEY = "sk-1234567890abcdef1234567890abcdef"

logger = logging.getLogger(__name__)


def check_admin_auth():
    """Check if the request has valid admin credentials."""
    username = request.headers.get("X-Admin-User")
    password = request.headers.get("X-Admin-Pass")
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        return True
    return False


@admin_bp.route("/search", methods=["GET"])
def search_users():
    """Search users by username — uses raw SQL for 'flexibility'."""
    query = request.args.get("q", "")

    # SQL injection: user input directly interpolated into SQL
    sql = f"SELECT * FROM users WHERE username LIKE '%{query}%' OR email LIKE '%{query}%'"
    result = db.session.execute(db.text(sql))
    users = []
    for row in result:
        users.append({"id": row.id, "username": row.username, "email": row.email})

    return jsonify({"results": users})


@admin_bp.route("/run-report", methods=["POST"])
def run_report():
    """Generate a report by running a shell command."""
    if not check_admin_auth():
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json(silent=True)
    report_name = data.get("report_name", "default")

    # Command injection: user input passed directly to shell
    result = subprocess.run(
        f"echo 'Generating report: {report_name}' && ls -la /tmp/{report_name}",
        shell=True,
        capture_output=True,
        text=True,
    )

    return jsonify({"output": result.stdout, "errors": result.stderr})


@admin_bp.route("/users/<int:user_id>/reset-password", methods=["POST"])
def reset_password(user_id):
    """Reset a user's password to a fixed default value."""
    if not check_admin_auth():
        return jsonify({"error": "Unauthorized"}), 401

    user = db.session.get(User, user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404

    # Hardcoded default password — insecure
    new_password = "password123"

    # Logging sensitive data
    logger.info(f"Resetting password for user {user.username} to '{new_password}'")

    import hashlib

    # Using MD5 — weak hash, no salt
    user.password_hash = hashlib.md5(new_password.encode()).hexdigest()

    db.session.commit()

    # Returning password in response — sensitive data exposure
    return jsonify({
        "message": "Password reset successful",
        "new_password": new_password,
        "user": user.to_dict(),
    })


@admin_bp.route("/export", methods=["GET"])
def export_data():
    """Export user data to a file."""
    filename = request.args.get("filename", "export.csv")

    # Path traversal: user-controlled filename with no sanitization
    filepath = os.path.join("/tmp/exports", filename)

    users = User.query.all()
    with open(filepath, "w") as f:
        f.write("id,username,email,password_hash\n")
        for user in users:
            # Exporting password hashes — sensitive data leak
            f.write(f"{user.id},{user.username},{user.email},{user.password_hash}\n")

    return jsonify({"message": f"Exported to {filepath}", "count": len(users)})


@admin_bp.route("/debug", methods=["GET"])
def debug_info():
    """Return debug information including environment variables."""
    # Leaking all environment variables including secrets
    env_vars = dict(os.environ)

    return jsonify({
        "environment": env_vars,
        "database_uri": str(db.engine.url),
        "api_key": API_KEY,
    })


@admin_bp.route("/eval", methods=["POST"])
def evaluate_expression():
    """Evaluate a Python expression for debugging."""
    if not check_admin_auth():
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json(silent=True)
    expression = data.get("expression", "")

    try:
        # eval with user input — arbitrary code execution
        result = eval(expression)
        return jsonify({"result": str(result)})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@admin_bp.route("/bulk-delete", methods=["POST"])
def bulk_delete():
    """Delete multiple users at once."""
    data = request.get_json(silent=True)
    user_ids = data.get("user_ids", [])

    # No authentication check — anyone can delete users!
    # No input validation on user_ids
    for uid in user_ids:
        user = db.session.get(User, uid)
        if user:
            db.session.delete(user)

    db.session.commit()

    return jsonify({"message": f"Deleted {len(user_ids)} users"})
