import asyncio
import sys

from gufo.snmp import SnmpSession
from typing import List, Dict, Any

COMMUNITY = "c13mw08m"
ADDRESS = "10.1.1.142"
OIDS = [
    "1.3.6.1.4.1.9.2.1.73.0",
    "1.3.6.1.2.1.47.1.1.1.1.2",
    "1.3.6.1.2.1.47.1.1.1.1.5",
    "1.3.6.1.2.1.47.1.1.1.1.7",
    "1.3.6.1.2.1.47.1.1.1.1.8",
    "1.3.6.1.2.1.47.1.1.1.1.9",
    "1.3.6.1.2.1.47.1.1.1.1.10",
    "1.3.6.1.2.1.47.1.1.1.1.11",
    "1.3.6.1.2.1.47.1.1.1.1.12",
    "1.3.6.1.2.1.47.1.1.1.1.13",
    "1.3.6.1.2.1.47.1.1.1.1.16",
]


async def snmp_get_and_bulk(addr: str, community: str, oids: List[str], timeout: float = 4.0) -> dict[Any, Any]:
    # sourcery skip: use-named-expression
    async with SnmpSession(addr=addr, community=community, timeout=timeout) as session:
        snmp_data = dict((await session.get_many(oids)).items())
        not_resolved_oids = [oid for oid in oids if oid not in snmp_data]
        if not_resolved_oids:
            for oid in not_resolved_oids:
                async for k, v in session.fetch(oid):
                    snmp_data |= {k: v}
        return snmp_data

asyncio.run(snmp_get_and_bulk(ADDRESS, COMMUNITY, OIDS))
