import random
from faker import Faker
from typing import List, Dict

# Initialize Faker for generating fake data
fake = Faker()

def generate_contacts(count: int = 100) -> List[Dict]:
    """Generate sample contacts data"""
    contacts = []
    for i in range(1, count + 1):
        contacts.append({
            "contact_id": f"CONTACT_{i:03d}",
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.email(),
            "phone": fake.phone_number(),
            "company": fake.company(),
            "job_title": fake.job(),
            "address": fake.address().replace("\n", ", ")
        })
    return contacts

def generate_deals(count: int = 100) -> List[Dict]:
    """Generate sample deals data"""
    deal_stages = ["Prospecting", "Qualification", "Negotiation", "Closed Won", "Closed Lost"]
    deal_types = ["New Business", "Existing Business", "Renewal", "Upsell"]
    
    deals = []
    for i in range(1, count + 1):
        # Randomly assign to existing contacts (some deals might not have contacts)
        contact_id = f"CONTACT_{random.randint(1, 120):03d}" if random.random() > 0.1 else None
        
        deals.append({
            "deal_id": f"DEAL_{i:03d}",
            "deal_name": f"Deal for {fake.word().title()} Project",
            "amount": round(random.uniform(1000, 50000), 2),
            "stage": random.choice(deal_stages),
            "type": random.choice(deal_types),
            "close_date": fake.date_between(start_date='-30d', end_date='+90d').isoformat(),
            "contact_id": contact_id,
            "probability": random.randint(0, 100),
            "description": fake.sentence()
        })
    return deals

def sync_deals_with_contacts(deals: List[Dict], contacts: List[Dict]) -> List[Dict]:
    """Sync deals with contacts based on contact_id"""
    # Create a contact lookup dictionary
    contact_lookup = {contact["contact_id"]: contact for contact in contacts}
    
    # Enrich deals with contact information
    synced_deals = []
    for deal in deals:
        deal_copy = deal.copy()
        if deal["contact_id"] and deal["contact_id"] in contact_lookup:
            deal_copy["contact"] = contact_lookup[deal["contact_id"]]
        else:
            deal_copy["contact"] = None
        synced_deals.append(deal_copy)
    
    return synced_deals

def main():
    # Generate sample data
    contacts = generate_contacts(100)
    deals = generate_deals(100)
    
    # Sync deals with contacts
    synced_deals = sync_deals_with_contacts(deals, contacts)
    
    # Print sample output
    print("Sample Synced Deals (first 5):")
    for deal in synced_deals[:5]:
        print(f"\nDeal ID: {deal['deal_id']}")
        print(f"Deal Name: {deal['deal_name']}")
        print(f"Amount: ${deal['amount']:,.2f}")
        print(f"Stage: {deal['stage']}")
        if deal['contact']:
            print(f"Contact: {deal['contact']['first_name']} {deal['contact']['last_name']}")
            print(f"Email: {deal['contact']['email']}")
            print(f"Company: {deal['contact']['company']}")
        else:
            print("Contact: No associated contact")
        print("-" * 50)

if __name__ == "__main__":
    main()
