import httpx


async def get_gig_status(tracking_id: str):
    url = f"https://api.dhl.ng/tracking/{tracking_id}"  # placeholder
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()
        return {
            "status": data.get("current_status"),
            "location": data.get("location"),
            "timestamp": data.get("updated_at"),
        }
