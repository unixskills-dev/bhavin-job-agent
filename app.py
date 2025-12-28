import json
import streamlit as st
from llm_client import call_llm_json
from prompts import MATCH_PROMPT, TAILORED_RESUME_PROMPT, RECRUITER_MESSAGE_PROMPT
# Load profile
with open("profile.json") as f:
    PROFILE = json.load(f)
BASE_HIGHLIGHTS = """
- 29+ years in UNIX/Linux, cloud, and hybrid infrastructure for large enterprises.
- 5+ years in IAM using Keycloak, FreeIPA, DigiCert, HashiCorp Vault, PrivacyIDEA, LDAP, SAML, OIDC, and RBAC.
- Cloud and container platforms: AWS, Azure, OpenStack (Neutron, Octavia, Manila, Cinder, Nova, Ironic, Glance), OpenShift, Docker, Kubernetes, Proxmox.
- Automation and DevOps: Ansible, AAP, Puppet, ArgoCD, Terraform, Git/GitHub/GitLab, Python, Bash, KSH.
- Monitoring and SRE: Splunk, SignalFx, Catchpoint, PagerDuty, Site24x7, Grafana, Zabbix, Nagios, OP5, Cacti, ELK, Prometheus.
- Virtualization, storage, and DR: VMware ESXi, vCenter, vCloud Director, HP/EMC/NetApp/Dell/IBM SAN/NAS, 3PAR, Data Domain, Ceph, MinIO, HP ServiceGuard, Oracle RAC.
"""
st.title("Bhavin Job Match Agent")
st.markdown("Paste a job description below to see how well it matches your profile and get tailored content.")
job_description = st.text_area("Job Description", height=300)
if st.button("Analyze & Generate") and job_description.strip():
    with st.spinner("Analyzing job match..."):
        profile_json = json.dumps(PROFILE, indent=2)
# 1. Match analysis
        match_prompt = MATCH_PROMPT.format(
            profile_json=profile_json,
            job_description=job_description
        )
        match_result = call_llm_json(match_prompt)
st.subheader("Match Analysis")
        st.json(match_result)
decision = match_result.get("apply_decision", "UNKNOWN")
        score = match_result.get("overall_score", 0)
        st.markdown(f"**Decision:** {decision}  |  **Score:** {score}")
if decision in ["YES", "MAYBE"]:
            # 2. Tailored resume content
            resume_prompt = TAILORED_RESUME_PROMPT.format(
                base_highlights=BASE_HIGHLIGHTS,
                job_description=job_description,
                match_json=json.dumps(match_result, indent=2)
            )
            tailored_resume = call_llm_json(resume_prompt)
st.subheader("Tailored Resume Summary & Bullets")
            st.markdown("**Summary:**")
            st.write(tailored_resume.get("summary", ""))
st.markdown("**Bullets:**")
            for bullet in tailored_resume.get("bullets", []):
                st.markdown(f"- {bullet}")
# 3. Recruiter message
            msg_prompt = RECRUITER_MESSAGE_PROMPT.format(
                job_description=job_description,
                match_json=json.dumps(match_result, indent=2)
            )
            recruiter_msg = call_llm_json(msg_prompt)
st.subheader("Recruiter Message")
            st.markdown("**Subject:**")
            st.write(recruiter_msg.get("subject", "Regarding Senior IAM / Infrastructure role"))
st.markdown("**Body:**")
            st.write(recruiter_msg.get("body", ""))
        else:
            st.info("Agent recommends skipping this role based on your preferences and profile."
