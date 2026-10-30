# EU CBAM Embedded Carbon Accounting & Tariff Estimator Skill

[![GenPark Official](https://img.shields.io/badge/GenPark-Official%20Skill-blue)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-GenPark-blue)](https://www.linkedin.com/company/92955550)
[![MCP Compliant](https://img.shields.io/badge/MCP-JSON--RPC%202.0-green)](https://modelcontextprotocol.io/)
[![Zero Dependency](https://img.shields.io/badge/Dependencies-Zero%20Stdlib-brightgreen)](https://python.org)

EU Carbon Border Adjustment Mechanism (CBAM) direct/indirect specific embedded emissions factor calculation (tCO2e/tonne) across imported goods. Built for GenPark (https://www.genpark.ai).

## Official Channels
- **Official Website**: [https://www.genpark.ai](https://www.genpark.ai)
- **LinkedIn Page**: [https://www.linkedin.com/company/92955550](https://www.linkedin.com/company/92955550)

## MCP Tools Exposed
- `calculate_cbam_embedded_carbon_liability`: Calculate CBAM certificate liability from imported tonnage, specific embedded emissions (tCO2e/tonne), and EU ETS carbon price.
- `generate_cbam_quarterly_reporting_payload`: Compile official XML/JSON reporting data block for EU CBAM Transitional Registry submission.

## Installation & Usage
```bash
python -m genpark_agentic_commerce_cbam_embedded_carbon_accounting_skill.server --test
```
