import pyziptax

pyziptax.api_key = "ASDF1234"
print(pyziptax.get_rate('10001', 'New York', 'NY', False))
# 8.875

print(pyziptax.get_rate('94304', multiple_rates=True))
# {u'LOCKHEED': Decimal('8.250'), u'PALO ALTO': Decimal('8.750')}
