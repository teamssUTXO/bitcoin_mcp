# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 1.0.x   | ✅         |

---

## Reporting Security Vulnerabilities

We take the security of this project seriously. If you believe you have discovered a security vulnerability, we appreciate yout help in disclosing it to us responsibly.

⚠️ **Please DO NOT create a public GitHub issue for security vulnerabilites**

To report a security vulnerability, send a private message to the maintainers : `teamsutxo` on Discord

### Information to Include

To help understand and resolve the vulnerability, please provide the following information:

- **Description**: A clear and detailed description of the vulnerability
- **Steps to Reproduce**: Step-by-step instructions demonstrating how to exploit the vulnerability
- **Impact Assessment**: Potentiel consequences if the vulnerability is exploited
- **Affected Components**: Specific parts of the codebase, versions, or configurations affected
- **Suggested Fix**: If you have ideas for fixing it

We will acknowledge receipt of your report within 24 hours

We aim to resolve critical vulnerabilities within 1 week

---

## Security Considerations for Users

To ensure secure API access and MCP server operations, please follow these best practices:

- **Environment Isolation**: Run MCP servers in isolated environments (containers, VMs, or sandboxed processes) when possible
- **File Permissions**: Restrict access to sensitive configuration files using `chmod 600 [CONFIG_FILE]`. 
- **Network Restrictions**: Limit network access to only required ports and protocols
- **Log Monitoring**: Regularly review server logs for suspicious activity or unauthorized access attempts
- **Dependency Security**: Use `uv check` to monitor for known vulnerabilities in packages