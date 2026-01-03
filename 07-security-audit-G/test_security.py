"""07-security-audit 测试"""
from engine import SecurityAuditor

def test_security_audit():
    print("=== 测试安全审计 ===\n")

    test_code = '''
password = "hardcoded123"
api_key = "AKIAIOSFODNN7EXAMPLE"
db.execute("SELECT * FROM users WHERE id = " + user_id)
'''

    with open('test_vuln.py', 'w') as f:
        f.write(test_code)

    auditor = SecurityAuditor()
    vulnerabilities = auditor.audit_file('test_vuln.py')

    print(f"发现 {len(vulnerabilities)} 个漏洞:")
    for vuln in vulnerabilities:
        print(f"  - {vuln.severity}: {vuln.description}")

    import os
    os.remove('test_vuln.py')

    print("\n✓ 测试通过")

if __name__ == '__main__':
    test_security_audit()
