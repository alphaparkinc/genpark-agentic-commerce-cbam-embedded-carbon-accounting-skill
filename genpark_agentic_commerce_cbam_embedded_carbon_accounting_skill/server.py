# -*- coding: utf-8 -*-
"""MCP Server for EU CBAM Embedded Carbon Accounting & Tariff Estimator Skill."""
import sys
import json
import logging
from typing import Dict, Any

from .core import EUCBAMEmbeddedCarbonAccountingEngine

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

TOOLS_SCHEMA = [
    {
        "name": "calculate_cbam_embedded_carbon_liability",
        "description": "Calculate CBAM certificate liability from imported tonnage, specific embedded emissions (tCO2e/tonne), and EU ETS carbon price.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "goods_category": {
                    "type": "string",
                    "enum": [
                        "steel",
                        "aluminum",
                        "cement",
                        "fertilizer",
                        "hydrogen"
                    ]
                },
                "imported_metric_tonnes": {
                    "type": "number"
                },
                "specific_embedded_emissions_tco2e_per_t": {
                    "type": "number"
                },
                "eu_ets_carbon_price_eur": {
                    "type": "number"
                },
                "carbon_price_paid_origin_eur": {
                    "type": "number"
                }
            },
            "required": [
                "goods_category",
                "imported_metric_tonnes",
                "specific_embedded_emissions_tco2e_per_t"
            ]
        }
    },
    {
        "name": "generate_cbam_quarterly_reporting_payload",
        "description": "Compile official XML/JSON reporting data block for EU CBAM Transitional Registry submission.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "importer_eori": {
                    "type": "string"
                },
                "installation_country": {
                    "type": "string"
                },
                "total_embedded_emissions_tco2e": {
                    "type": "number"
                }
            },
            "required": [
                "importer_eori",
                "installation_country",
                "total_embedded_emissions_tco2e"
            ]
        }
    }
]

def handle_rpc(line: str) -> str:
    try:
        req = json.loads(line)
        method = req.get("method")
        msg_id = req.get("id")

        if method == "initialize":
            res = {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-agentic-commerce-cbam-embedded-carbon-accounting-skill", "version": "1.0.0"}
            }
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": res})

        elif method == "tools/list":
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"tools": TOOLS_SCHEMA}})

        elif method == "tools/call":
            params = req.get("params", {})
            tool_name = params.get("name")
            args = params.get("arguments", {})

            target_func = getattr(EUCBAMEmbeddedCarbonAccountingEngine, tool_name, None)
            if not target_func:
                return json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": f"Method not found: {tool_name}"}})

            result = target_func(**args)
            return json.dumps({
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps(result, indent=2)}]
                }
            })

        else:
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": f"Method not found: {method}"}})

    except Exception as e:
        return json.dumps({"jsonrpc": "2.0", "id": req.get("id") if "req" in locals() else None, "error": {"code": -32000, "message": str(e)}})

def run_test():
    init_req = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}})
    init_res = json.loads(handle_rpc(init_req))
    assert init_res.get("result", {}).get("serverInfo", {}).get("name") == "genpark-agentic-commerce-cbam-embedded-carbon-accounting-skill"

    list_req = json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
    list_res = json.loads(handle_rpc(list_req))
    assert len(list_res.get("result", {}).get("tools", [])) == 2
    return True

if __name__ == "__main__":
    if "--test" in sys.argv:
        if run_test():
            sys.exit(0)
        sys.exit(1)

    for line in sys.stdin:
        if not line.strip():
            continue
        out = handle_rpc(line)
        sys.stdout.write(out + "\n")
        sys.stdout.flush()
