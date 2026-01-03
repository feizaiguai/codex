"""
UltraThink Configuration
配置文件
"""

from typing import Dict, Any


class UltraThinkConfig:
    """UltraThink main configuration"""

    # ============ Version ============
    VERSION = "1.0.0"

    # ============ Depth Level Configuration ============

    DEPTH_CONFIGS = {
        "quick": {
            "target_time_seconds": 45,  # 30-60s
            "target_pages": 8,  # 5-10 pages
            "phases": ["discover", "define", "decompose"],
            "detail_level": "high_level",
            "examples_per_section": 2
        },
        "standard": {
            "target_time_seconds": 135,  # 90-180s
            "target_pages": 22,  # 15-30 pages
            "phases": ["discover", "define", "design", "decompose", "declare"],
            "detail_level": "detailed",
            "examples_per_section": 3
        },
        "comprehensive": {
            "target_time_seconds": 240,  # 180-300s
            "target_pages": 30,  # 25-35 pages (reduced to avoid 50k token limit)
            "phases": ["discover", "define", "design", "decompose", "declare", "document"],
            "detail_level": "comprehensive",
            "examples_per_section": 3  # Reduced from 5 to avoid token overflow
        }
    }

    # ============ Quality Thresholds ============

    QUALITY_THRESHOLDS = {
        "A+": {
            "completeness_min": 95,
            "consistency_min": 100,
            "feasibility_min": 90,
            "gates_passed_min": 6
        },
        "A": {
            "completeness_min": 90,
            "consistency_min": 95,
            "feasibility_min": 85,
            "gates_passed_min": 6
        },
        "B": {
            "completeness_min": 80,
            "consistency_min": 90,
            "feasibility_min": 75,
            "gates_passed_min": 5
        },
        "C": {
            "completeness_min": 70,
            "consistency_min": 80,
            "feasibility_min": 65,
            "gates_passed_min": 4
        },
        "D": {
            "completeness_min": 0,
            "consistency_min": 0,
            "feasibility_min": 0,
            "gates_passed_min": 0
        }
    }

    # ============ Phase Gates ============

    PHASE_GATES = {
        "discover": {
            "name": "Business Clarity Check",
            "required_fields": [
                "stakeholders",
                "business_goals",
                "success_criteria"
            ],
            "min_items": {
                "stakeholders": 2,
                "business_goals": 1,
                "success_criteria": 1
            }
        },
        "define": {
            "name": "Requirements Validation",
            "required_fields": [
                "functional_requirements",
                "non_functional_requirements",
                "bdd_scenarios"
            ],
            "min_items": {
                "functional_requirements": 5,
                "non_functional_requirements": 3,
                "bdd_scenarios": 3
            }
        },
        "design": {
            "name": "Architecture Review",
            "required_fields": [
                "domain_model",
                "architecture_pattern",
                "tech_stack",
                "adrs"
            ],
            "min_items": {
                "tech_stack": 3,
                "adrs": 2
            }
        },
        "decompose": {
            "name": "Feasibility Check",
            "required_fields": [
                "wbs",
                "pert_estimates",
                "milestones"
            ],
            "min_items": {
                "wbs": 10,
                "milestones": 3
            }
        },
        "declare": {
            "name": "Testability Check",
            "required_fields": [
                "test_pyramid",
                "test_specs",
                "performance_benchmarks"
            ],
            "min_items": {
                "test_specs": 10,
                "performance_benchmarks": 3
            }
        },
        "document": {
            "name": "Completeness Check",
            "required_fields": [
                "markdown_spec",
                "quality_metrics"
            ],
            "min_items": {}
        }
    }

    # ============ Validation Rules ============

    VALIDATION_RULES = {
        "conflict_detection": {
            "enabled": True,
            "check_types": [
                "requirement_conflicts",
                "architecture_mismatches",
                "resource_conflicts",
                "timeline_conflicts"
            ]
        },
        "consistency_check": {
            "enabled": True,
            "check_types": [
                "terminology",
                "data_model",
                "api_contracts",
                "test_coverage"
            ]
        },
        "completeness_check": {
            "enabled": True,
            "required_coverage": {
                "business_context": 0.95,
                "requirements": 0.90,
                "design": 0.90,
                "planning": 0.85,
                "testing": 0.90
            }
        }
    }

    # ============ Template Configuration ============

    TEMPLATE_SECTIONS = {
        "business_context": [
            "stakeholders",
            "business_goals",
            "success_metrics",
            "constraints",
            "assumptions"
        ],
        "requirements": [
            "functional_requirements",
            "non_functional_requirements",
            "user_stories",
            "bdd_scenarios",
            "api_contracts",
            "glossary"
        ],
        "design": [
            "domain_model",
            "bounded_contexts",
            "architecture_pattern",
            "architecture_diagram",
            "tech_stack",
            "adrs",
            "risk_assessment"
        ],
        "implementation_plan": [
            "wbs",
            "feature_prioritization",
            "pert_estimates",
            "critical_path",
            "milestones",
            "resource_allocation",
            "timeline"
        ],
        "test_strategy": [
            "test_pyramid",
            "tdd_specs",
            "integration_tests",
            "performance_benchmarks",
            "security_validations",
            "test_coverage"
        ],
        "appendix": [
            "glossary",
            "references",
            "version_history",
            "quality_report"
        ]
    }

    # ============ BDD Templates ============

    BDD_TEMPLATES = {
        "user_authentication": """
Feature: User Authentication
  As a user
  I want to securely log in to the system
  So that I can access my personal data

Scenario: Successful login with valid credentials
  Given I am on the login page
  And I have a valid account with username "user@example.com"
  When I enter my username and password
  And I click the "Login" button
  Then I should be redirected to the dashboard
  And I should see a welcome message with my name
        """,

        "api_endpoint": """
Feature: API Endpoint - {endpoint}
  As an API consumer
  I want to {action}
  So that {benefit}

Scenario: Successful request
  Given I have a valid API key
  When I send a {method} request to "{endpoint}"
  Then I should receive a 200 OK response
  And the response should contain {expected_data}
        """
    }

    # ============ DDD Patterns ============

    DDD_PATTERNS = {
        "entity": {
            "required_fields": ["id", "attributes", "behaviors"],
            "example": {
                "name": "Order",
                "attributes": ["id", "customer_id", "items", "total", "status", "created_at"],
                "behaviors": ["calculate_total", "add_item", "remove_item", "submit", "cancel"]
            }
        },
        "value_object": {
            "required_fields": ["attributes", "validation"],
            "example": {
                "name": "Address",
                "attributes": ["street", "city", "state", "zip_code", "country"],
                "validation": ["validate_zip_code", "validate_country"]
            }
        },
        "aggregate": {
            "required_fields": ["root_entity", "entities", "invariants"],
            "example": {
                "name": "OrderAggregate",
                "root_entity": "Order",
                "entities": ["OrderItem", "Payment", "Shipment"],
                "invariants": ["Order must have at least one item", "Total must match sum of items"]
            }
        }
    }

    # ============ Architecture Patterns ============

    ARCHITECTURE_PATTERNS = {
        "microservices": {
            "description": "Distributed services with independent deployment",
            "pros": ["Scalability", "Technology diversity", "Independent deployment"],
            "cons": ["Complexity", "Distributed transactions", "Network latency"],
            "when_to_use": "Large teams, multiple domains, high scalability needs"
        },
        "monolith": {
            "description": "Single deployable application",
            "pros": ["Simplicity", "Easy deployment", "Shared resources"],
            "cons": ["Limited scalability", "Tight coupling", "Large codebase"],
            "when_to_use": "Small teams, single domain, early stage"
        },
        "event_driven": {
            "description": "Event-based communication between components",
            "pros": ["Loose coupling", "Asynchronous processing", "Scalability"],
            "cons": ["Eventual consistency", "Complex debugging", "Event ordering"],
            "when_to_use": "Real-time systems, high-volume data processing"
        },
        "serverless": {
            "description": "Function-as-a-Service execution model",
            "pros": ["Auto-scaling", "Pay-per-use", "No server management"],
            "cons": ["Cold starts", "Vendor lock-in", "Limited execution time"],
            "when_to_use": "Variable load, event-driven, stateless operations"
        }
    }

    # ============ Test Pyramid Configuration ============

    TEST_PYRAMID = {
        "unit": {
            "percentage": 70,
            "description": "Fast, isolated tests for individual components",
            "framework_examples": ["Jest", "JUnit", "pytest", "Mocha"]
        },
        "integration": {
            "percentage": 20,
            "description": "Tests for component interactions",
            "framework_examples": ["Supertest", "TestContainers", "Postman"]
        },
        "e2e": {
            "percentage": 10,
            "description": "End-to-end user journey tests",
            "framework_examples": ["Cypress", "Selenium", "Playwright", "Puppeteer"]
        }
    }

    # ============ Estimation Constants ============

    ESTIMATION = {
        "complexity_multipliers": {
            "simple": 1.0,
            "medium": 1.5,
            "complex": 2.5,
            "very_complex": 4.0
        },
        "pert_formula": {
            "weight_optimistic": 1,
            "weight_most_likely": 4,
            "weight_pessimistic": 1,
            "divisor": 6
        },
        "buffer_percentage": 20,  # Add 20% buffer to estimates
        "resource_utilization_target": 0.80,  # 80% utilization (20% buffer)
        "hours_per_week": 40,
        "work_weeks_per_month": 4.33
    }

    # ============ Risk Categories ============

    RISK_CATEGORIES = {
        "technical": {
            "description": "Technology-related risks",
            "examples": ["New technology", "Integration complexity", "Performance"]
        },
        "business": {
            "description": "Business-related risks",
            "examples": ["Market changes", "Competition", "ROI uncertainty"]
        },
        "resource": {
            "description": "Resource-related risks",
            "examples": ["Team availability", "Skill gaps", "Budget constraints"]
        },
        "schedule": {
            "description": "Timeline-related risks",
            "examples": ["Dependencies", "Underestimation", "Scope creep"]
        },
        "regulatory": {
            "description": "Compliance-related risks",
            "examples": ["GDPR", "HIPAA", "SOC 2", "PCI-DSS"]
        }
    }

    # ============ Integration Configuration ============

    SKILL_INTEGRATION = {
        "01-requirements": {
            "can_invoke": True,
            "use_cases": ["Detailed BDD scenarios", "DDD modeling", "API contracts"]
        },
        "02-architecture": {
            "can_invoke": True,
            "use_cases": ["Tech stack evaluation", "Architecture patterns", "ADR templates"]
        },
        "29-project-planner": {
            "can_invoke": True,
            "use_cases": ["Detailed WBS", "Gantt charts", "Resource optimization"]
        },
        "15-web-search-G": {
            "can_invoke": True,
            "use_cases": ["Tech research", "Best practices", "Pattern validation"]
        }
    }

    # ============ Output Configuration ============

    OUTPUT_CONFIG = {
        "markdown": {
            "enabled": True,
            "include_toc": True,
            "include_diagrams": True,
            "max_depth": 4
        },
        "json": {
            "enabled": True,
            "pretty_print": True,
            "indent": 2
        },
        "diagrams": {
            "format": "mermaid",
            "types": ["domain_model", "architecture", "workflow", "erd", "gantt"]
        }
    }

    # ============ Completeness Weights ============

    COMPLETENESS_WEIGHTS = {
        "business_context": 0.15,
        "requirements": 0.25,
        "design": 0.25,
        "implementation_plan": 0.20,
        "test_strategy": 0.15
    }

    @classmethod
    def get_depth_config(cls, depth: str) -> Dict[str, Any]:
        """Get configuration for specified depth level"""
        return cls.DEPTH_CONFIGS.get(depth, cls.DEPTH_CONFIGS["standard"])

    @classmethod
    def get_quality_threshold(cls, grade: str) -> Dict[str, Any]:
        """Get quality threshold for specified grade"""
        return cls.QUALITY_THRESHOLDS.get(grade, cls.QUALITY_THRESHOLDS["D"])

    @classmethod
    def calculate_quality_grade(
        cls,
        completeness: float,
        consistency: float,
        feasibility: float,
        gates_passed: int
    ) -> str:
        """Calculate quality grade based on metrics"""

        for grade in ["A+", "A", "B", "C", "D"]:
            threshold = cls.get_quality_threshold(grade)

            if (completeness >= threshold["completeness_min"] and
                consistency >= threshold["consistency_min"] and
                feasibility >= threshold["feasibility_min"] and
                gates_passed >= threshold["gates_passed_min"]):
                return grade

        return "D"
