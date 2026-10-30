import click
from getpass import getpass
from app.extensions import db, hash_password
from app.models.user import User

def register_cli_commands(app):
    @app.cli.command("create-admin")
    def create_admin():
        """Create a secure administrator account by prompting interactively."""
        click.echo("=== Create Secure Administrator Account ===")
        full_name = click.prompt("Admin Full Name", default="System Administrator")
        email = click.prompt("Admin Email Address").strip().lower()

        existing = User.query.filter_by(email=email).first()
        if existing:
            click.echo(f"Error: User with email '{email}' already exists.")
            return

        while True:
            password = getpass("Enter Admin Password (min 8 chars): ")
            if len(password) < 8:
                click.echo("Password must be at least 8 characters.")
                continue
            confirm = getpass("Confirm Admin Password: ")
            if password != confirm:
                click.echo("Passwords do not match. Try again.")
                continue
            break

        admin = User(
            full_name=full_name,
            email=email,
            password_hash=hash_password(password),
            role="admin",
            preferred_language="en",
        )
        db.session.add(admin)
        db.session.commit()
        click.echo(f"[OK] Administrator account for '{email}' created successfully.")

    @app.cli.command("seed-db")
    @click.option("--content-only", is_flag=True, help="Seed only agricultural crops and guides (no demo users)")
    @click.option("--with-demo-users", is_flag=True, help="Seed development demo student and admin users")
    def seed_db_command(content_only, with_demo_users):
        """Seed the database with agricultural crops, guides, products, and quizzes."""
        from seed.seed import seed_database
        with_users = with_demo_users or (not content_only)
        seed_database(content_only=content_only, with_demo_users=with_users)
