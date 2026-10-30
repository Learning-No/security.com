# Security Architecture

A practical security architecture knowledge base and reference blueprint. The interface takes visual inspiration from compact, panel-based browser dashboards, while using original branding, layout details, and content.

## Purpose

This project is an educational workspace for understanding how to design, document, and govern secure systems. It is organised around architecture layers, security domains, trust boundaries, threat modelling, controls, and implementation planning.

## Current site sections

- **Overview** — architecture summary, core principles, and priority design considerations.
- **Reference blueprint** — identity and endpoints, edge, network, applications, data, and security operations.
- **Security domains** — searchable capability directory across protection, detection, and governance.
- **Threat model** — STRIDE prompts, risk examples, and a threat-modelling workflow.
- **Controls library** — identity, network, application, data, detection, and governance safeguards.
- **Roadmap** — a staged path from discovery through continuous assurance.
- **Resources** — links to NIST, CIS, OWASP, MITRE ATT&CK, and Cloud Security Alliance.

## Run locally

The site is a static HTML/CSS/JavaScript frontend and can be opened directly in a browser. For the existing FastAPI development service, install the packages in `requirements.txt`, set a random `SECRET_KEY` of at least 32 characters, and run:

```bash
uvicorn app.main:app --reload
```

Then open `http://127.0.0.1:8000/`.

The repository retains an early FastAPI/PostgreSQL account and activity prototype from its previous Ironhaven experiment. The current architecture knowledge-base frontend does not depend on those game endpoints. Treat that backend as a separate development component until it is deliberately redesigned around architecture documentation, user workspaces, and access control.

## Architecture guidance

The diagrams and control examples are illustrative starting points, not a certified design or a guarantee of compliance. Tailor them to the system context, threat model, data classification, business requirements, and applicable laws and standards.

## Security references

- [NIST Cybersecurity Framework 2.0](https://www.nist.gov/cyberframework)
- [NIST SP 800-207 — Zero Trust Architecture](https://csrc.nist.gov/pubs/sp/800/207/final)
- [CIS Critical Security Controls](https://www.cisecurity.org/controls)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [MITRE ATT&CK](https://attack.mitre.org/)
- [Cloud Security Alliance](https://cloudsecurityalliance.org/)

## Project structure

```
index.html
app/
  main.py
  config.py
  database.py
  models.py
  schemas.py
  security.py
  dependencies.py
  routes/
requirements.txt
Dockerfile
docker-compose.yml
.env.example
.github/workflows/backend-checks.yml
```

## Status

The frontend has an initial architecture dashboard and interactive section navigation/search. The existing backend has not yet been converted into a content-management or multi-user architecture documentation service. Production deployment, accessibility review, browser testing, backend redesign, and security review remain future work.
