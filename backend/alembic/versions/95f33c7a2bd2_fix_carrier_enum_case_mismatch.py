"""fix carrier enum case mismatch

Revision ID: 95f33c7a2bd2
Revises: 7e6085d416af
Create Date: 2025-10-13 16:07:11.056907

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "95f33c7a2bd2"
down_revision: Union[str, Sequence[str], None] = "7e6085d416af"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # 1. Create a new enum type with lowercase values
    op.execute(
        "CREATE TYPE carriertype_new AS ENUM ('api', 'webhook', 'scraper', 'manual')"
    )

    # 2. Alter the carrier table to use the new enum
    op.execute(
        """
        ALTER TABLE carrier
        ALTER COLUMN type DROP DEFAULT,
        ALTER COLUMN type TYPE carriertype_new
        USING LOWER(type::text)::carriertype_new
    """
    )

    # 3. Drop the old enum type and rename the new one
    op.execute("DROP TYPE carriertype")
    op.execute("ALTER TYPE carriertype_new RENAME TO carriertype")

    # 4. Re-add default
    op.execute("ALTER TABLE carrier ALTER COLUMN type SET DEFAULT 'api'")


def downgrade():
    # Recreate the old enum type with uppercase values
    op.execute(
        "CREATE TYPE carriertype_old AS ENUM ('API', 'WEBHOOK', 'SCRAPER', 'MANUAL')"
    )

    op.execute(
        """
        ALTER TABLE carrier
        ALTER COLUMN type DROP DEFAULT,
        ALTER COLUMN type TYPE carriertype_old
        USING UPPER(type::text)::carriertype_old
    """
    )

    op.execute("DROP TYPE carriertype")
    op.execute("ALTER TYPE carriertype_old RENAME TO carriertype")

    op.execute("ALTER TABLE carrier ALTER COLUMN type SET DEFAULT 'API'")
