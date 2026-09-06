import asyncio
import os
import sys
import uuid
import argparse
from sqlalchemy import select

# Add backend directory to sys.path
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend'))
sys.path.append(backend_path)

from app.database import init_db
from app.models.user import User
from app.core.security import hash_password

DEFAULT_EMAIL = os.getenv("ADMIN_EMAIL", "admin@ayurveda-ipr.gov.in")
DEFAULT_PASSWORD = os.getenv("ADMIN_PASSWORD", "AdminSecurePassword2026!")
DEFAULT_NAME = os.getenv("ADMIN_NAME", "Ayurvedic IPR System Administrator")

async def seed_or_update_admin(email: str, password: str, full_name: str):
    await init_db()
    from app.database import async_session_maker
    async with async_session_maker() as session:
        try:
            # Check if user already exists
            result = await session.execute(select(User).where(User.email == email))
            existing_user = result.scalars().first()

            if existing_user:
                # Update existing user's password and ensure ADMIN role
                existing_user.password_hash = hash_password(password)
                existing_user.full_name = full_name
                existing_user.role = "ADMIN"
                existing_user.is_active = True
                await session.commit()
                print(f"[SUCCESS] Updated existing admin user:")
                print(f"  Email:    {email}")
                print(f"  Password: {password} (Updated)")
                print(f"  Role:     ADMIN")
                return

            # Create new admin user
            admin_user = User(
                id=uuid.uuid4(),
                email=email,
                password_hash=hash_password(password),
                full_name=full_name,
                role="ADMIN",
                preferred_language="en",
                is_active=True
            )
            session.add(admin_user)
            await session.commit()
            print(f"[SUCCESS] Created new admin user successfully:")
            print(f"  Email:    {email}")
            print(f"  Password: {password}")
            print(f"  Role:     ADMIN")
        except Exception as e:
            print(f"[ERROR] Failed to create or update admin user: {e}")
            await session.rollback()

def main():
    parser = argparse.ArgumentParser(description="Seed or update Ayurvedic IPR Administrator credentials.")
    parser.add_argument("--email", type=str, default=DEFAULT_EMAIL, help="Admin email address")
    parser.add_argument("--password", type=str, default=DEFAULT_PASSWORD, help="Admin password (min 8 characters)")
    parser.add_argument("--name", type=str, default=DEFAULT_NAME, help="Admin display name")
    args = parser.parse_args()

    asyncio.run(seed_or_update_admin(args.email, args.password, args.name))

if __name__ == "__main__":
    main()
