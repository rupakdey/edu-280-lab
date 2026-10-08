/* EDU-280 pilot: only published labs belong in labs[]. Planned Labs 2–9 link to Course Index anchors; source Lab 0 appears as a checkpoint. No session passwords or activation/provisioning codes are stored. */
window.LAB_GUIDE_COURSE = {
  "id": "EDU-280",
  "title": "Zscaler Zero Trust Branch",
  "subtitle": "Unofficial Web Lab Guide",
  "storagePrefix": "edu280",
  "labAccess": {
    "title": "Lab Access · Getting Started",
    "href": "index.html#lab-access"
  },
  "sdcAccess": null,
  "labs": [
    {
      "number": 1,
      "title": "Zero Trust Branch Device Interface Configuration",
      "href": "lab-01.html",
      "optional": false,
      "sdc": false,
      "keywords": "Zero Trust Branch ZTB high availability branch HA provisioning site DHCP NAT DNS VRRP App Connector",
      "tasks": [
        {
          "number": "1.1",
          "id": "task-1-1",
          "title": "Add Site",
          "href": "lab-01.html#task-1-1",
          "keywords": "site template vm-ha"
        },
        {
          "number": "1.2",
          "id": "task-1-2",
          "title": "Activate the Active Device",
          "href": "lab-01.html#task-1-2",
          "keywords": "primary gateway activation"
        },
        {
          "number": "1.3",
          "id": "task-1-3",
          "title": "Activate the Standby Device",
          "href": "lab-01.html#task-1-3",
          "keywords": "secondary gateway activation standby"
        },
        {
          "number": "1.4",
          "id": "task-1-4",
          "title": "Validate and Configure Site-Level Settings",
          "href": "lab-01.html#task-1-4",
          "keywords": "debug DNS NAT VRRP DHCP IPSec ZPA"
        }
      ],
      "explainers": [
        {
          "id": "ztb-ha-context",
          "title": "Zero Trust Branch HA architecture",
          "href": "lab-01.html#ztb-ha-context",
          "keywords": "network architecture topology active standby"
        }
      ]
    }
  ],
  "search": [
    {
      "label": "Lab foundation / topology",
      "href": "index.html#environment",
      "keywords": "lab network VLAN ZTB DIA Zero Trust Exchange"
    },
    {
      "label": "Lab 2 · Secure Internal Communication (Inter-VLAN Traffic Filtering) (planned)",
      "href": "index.html#lab-2",
      "keywords": "Implement macrosegmentation and site-level inter-VLAN policy. planned source index"
    },
    {
      "label": "Lab 3 · Validate Securing Internal and External Communication Policies (planned)",
      "href": "index.html#lab-3",
      "keywords": "Validate cloud forwarding, DNS, outbound connectivity, and ZPA access. planned source index"
    },
    {
      "label": "Lab 4 · Configure Microsegmentation Policy (planned)",
      "href": "index.html#lab-4",
      "keywords": "Enforce targeted protections between OT endpoints. planned source index"
    },
    {
      "label": "Lab 5 · Configure Policy-Based Routing (PBR) Policies (planned)",
      "href": "index.html#lab-5",
      "keywords": "Test cloud-forwarded traffic and configure direct ICMP routing. planned source index"
    },
    {
      "label": "Lab 6 · Configure DNS Policies (planned)",
      "href": "index.html#lab-6",
      "keywords": "Redirect and block selected domain traffic using DNS policy. planned source index"
    },
    {
      "label": "Lab 7 · Logs and Monitoring (planned · optional)",
      "href": "index.html#lab-7",
      "keywords": "Review packets, flows, alarms, and web insights. planned source index"
    },
    {
      "label": "Lab 8 · Troubleshoot and Debug Zero Trust Branch Environment (planned · optional)",
      "href": "index.html#lab-8",
      "keywords": "Use interface and system diagnostics for investigation. planned source index"
    },
    {
      "label": "Lab 9 · Configure Ransomware Kill Switch Policy (planned · optional)",
      "href": "index.html#lab-9",
      "keywords": "Configure SSH policies and test the ransomware kill switch. planned source index"
    }
  ]
};
