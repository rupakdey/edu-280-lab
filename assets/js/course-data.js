/* Course-specific EDU-280 navigation. All nine labs published; Labs 7–9 are optional. No session secrets. */
window.LAB_GUIDE_COURSE = {
  "id": "EDU-280",
  "title": "Zscaler Zero Trust Branch",
  "subtitle": "ZTB Lab Guide",
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
        },
        {
          "number": "1.5",
          "id": "task-1-5",
          "title": "Open interface configuration",
          "href": "lab-01.html#task-1-5",
          "keywords": "interfaces vlan lan wan DHCP gateway"
        },
        {
          "number": "1.6",
          "id": "task-1-6",
          "title": "Configure LAN GE6 / Subnet10",
          "href": "lab-01.html#task-1-6",
          "keywords": "interfaces vlan lan wan DHCP gateway"
        },
        {
          "number": "1.7",
          "id": "task-1-7",
          "title": "Configure LAN GE7 / Subnet20",
          "href": "lab-01.html#task-1-7",
          "keywords": "interfaces vlan lan wan DHCP gateway"
        },
        {
          "number": "1.8",
          "id": "task-1-8",
          "title": "Configure LAN GE8 / Subnet30",
          "href": "lab-01.html#task-1-8",
          "keywords": "interfaces vlan lan wan DHCP gateway"
        },
        {
          "number": "1.9",
          "id": "task-1-9",
          "title": "Configure secondary WAN GE2",
          "href": "lab-01.html#task-1-9",
          "keywords": "interfaces vlan lan wan DHCP gateway"
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
    },
    {
      "number": 2,
      "title": "Secure Internal Communication (Inter-VLAN Traffic Filtering)",
      "href": "lab-02.html",
      "optional": false,
      "sdc": false,
      "keywords": "Observe default inter-VLAN forwarding, apply macrosegmentation policies, and create a site-level OT-to-IoT exception.",
      "tasks": [
        {
          "number": "2.1",
          "id": "task-2-1",
          "title": "Verify default inter-VLAN communication",
          "href": "lab-02.html#task-2-1"
        },
        {
          "number": "2.2",
          "id": "task-2-2",
          "title": "Block Subnet10 to Subnet20 with macrosegmentation",
          "href": "lab-02.html#task-2-2"
        },
        {
          "number": "2.3",
          "id": "task-2-3",
          "title": "Allow OT-to-IoT at the site level",
          "href": "lab-02.html#task-2-3"
        }
      ],
      "explainers": [
        {
          "id": "macrosegmentation-context",
          "title": "Why macrosegmentation matters",
          "href": "lab-02.html#macrosegmentation-context",
          "keywords": "Each VLAN represents a broad workload group. A ZTB firewall policy can control traffic that crosses these groups, allowi"
        }
      ]
    },
    {
      "number": 3,
      "title": "Validate Securing Internal and External Communication Policies",
      "href": "lab-03.html",
      "optional": false,
      "sdc": false,
      "keywords": "Test ZIA forwarding, private app connectivity and remote ZPA access from the lab endpoints.",
      "tasks": [
        {
          "number": "3.1",
          "id": "task-3-1",
          "title": "Validate Windows server connectivity",
          "href": "lab-03.html#task-3-1"
        },
        {
          "number": "3.2",
          "id": "task-3-2",
          "title": "Access the Windows server remotely through ZPA",
          "href": "lab-03.html#task-3-2"
        },
        {
          "number": "3.3",
          "id": "task-3-3",
          "title": "Optional: Validate the IoT Ubuntu host",
          "href": "lab-03.html#task-3-3"
        },
        {
          "number": "3.4",
          "id": "task-3-4",
          "title": "Optional: Validate the OT Ubuntu host",
          "href": "lab-03.html#task-3-4"
        }
      ],
      "explainers": []
    },
    {
      "number": 4,
      "title": "Configure Microsegmentation Policy",
      "href": "lab-04.html",
      "optional": false,
      "sdc": false,
      "keywords": "Apply targeted isolation between OT endpoints within Subnet30.",
      "tasks": [
        {
          "number": "4.1",
          "id": "task-4-1",
          "title": "Verify baseline OT endpoint reachability",
          "href": "lab-04.html#task-4-1"
        },
        {
          "number": "4.2",
          "id": "task-4-2",
          "title": "Reject traffic between OT endpoints",
          "href": "lab-04.html#task-4-2"
        },
        {
          "number": "4.3",
          "id": "task-4-3",
          "title": "Verify OT-to-OT isolation",
          "href": "lab-04.html#task-4-3"
        }
      ],
      "explainers": [
        {
          "id": "microsegmentation-context",
          "title": "Macro versus microsegmentation",
          "href": "lab-04.html#microsegmentation-context",
          "keywords": "Macrosegmentation governs broad groups such as Subnet10, Subnet20 and Subnet30. Microsegmentation narrows the boundary t"
        }
      ]
    },
    {
      "number": 5,
      "title": "Configure Policy-Based Routing (PBR) Policies",
      "href": "lab-05.html",
      "optional": false,
      "sdc": false,
      "keywords": "Build a source- and application-specific ICMP route through the best direct WAN interface.",
      "tasks": [
        {
          "number": "5.1",
          "id": "task-5-1",
          "title": "Confirm baseline cloud forwarding",
          "href": "lab-05.html#task-5-1"
        },
        {
          "number": "5.2",
          "id": "task-5-2",
          "title": "Create SaaS object and direct-ICMP PBR policy",
          "href": "lab-05.html#task-5-2"
        },
        {
          "number": "5.3",
          "id": "task-5-3",
          "title": "Validate path selection and packet routing",
          "href": "lab-05.html#task-5-3"
        }
      ],
      "explainers": [
        {
          "id": "pbr-context",
          "title": "How policy-based routing selects a path",
          "href": "lab-05.html#pbr-context",
          "keywords": "A routing rule can match more than a destination network. The source exercise combines Subnet10, an Adobe SaaS applicati"
        }
      ]
    },
    {
      "number": 6,
      "title": "Configure DNS Policies",
      "href": "lab-06.html",
      "optional": false,
      "sdc": false,
      "keywords": "Use source-scoped DNS Override and Reject policies to control Google and WhatsApp resolution.",
      "tasks": [
        {
          "number": "6.1",
          "id": "task-6-1",
          "title": "Override Google DNS responses for OT1",
          "href": "lab-06.html#task-6-1"
        },
        {
          "number": "6.2",
          "id": "task-6-2",
          "title": "Reject WhatsApp DNS requests from the IoT subnet",
          "href": "lab-06.html#task-6-2"
        }
      ],
      "explainers": [
        {
          "id": "dns-policy-context",
          "title": "DNS response handling in the branch",
          "href": "lab-06.html#dns-policy-context",
          "keywords": "DNS rules inspect a request’s source and destination name before returning or forwarding an answer. The Google exercise "
        }
      ]
    },
    {
      "number": 7,
      "title": "Logs and Monitoring",
      "href": "lab-07.html",
      "optional": true,
      "sdc": false,
      "keywords": "Examine Packet Logs, Flow Logs, site alarms, and ZIA Web Insights for the assigned POD. optional",
      "tasks": [
        {
          "number": "7.1",
          "id": "task-7-1",
          "title": "View packet logs",
          "href": "lab-07.html#task-7-1"
        },
        {
          "number": "7.2",
          "id": "task-7-2",
          "title": "View flow logs",
          "href": "lab-07.html#task-7-2"
        },
        {
          "number": "7.3",
          "id": "task-7-3",
          "title": "Review Zero Trust Branch alarms",
          "href": "lab-07.html#task-7-3"
        },
        {
          "number": "7.4",
          "id": "task-7-4",
          "title": "Query POD web logs in Experience Center",
          "href": "lab-07.html#task-7-4"
        }
      ],
      "explainers": []
    },
    {
      "number": 8,
      "title": "Troubleshoot and Debug Zero Trust Branch Environment",
      "href": "lab-08.html",
      "optional": true,
      "sdc": false,
      "keywords": "Use appliance console diagnostics to inspect interfaces, routes, VRRP, IPSec, and live ICMP traffic. optional",
      "tasks": [
        {
          "number": "8.1",
          "id": "task-8-1",
          "title": "Inspect interfaces and routing",
          "href": "lab-08.html#task-8-1"
        },
        {
          "number": "8.2",
          "id": "task-8-2",
          "title": "Inspect gateway services and capture traffic",
          "href": "lab-08.html#task-8-2"
        }
      ],
      "explainers": []
    },
    {
      "number": 9,
      "title": "Configure Ransomware Kill Switch Policy",
      "href": "lab-09.html",
      "optional": true,
      "sdc": false,
      "keywords": "Stage Green/Orange SSH rules, test incident-response containment, then restore normal mode. optional",
      "tasks": [
        {
          "number": "9.1",
          "id": "task-9-1",
          "title": "Create and validate Green-mode SSH access",
          "href": "lab-09.html#task-9-1"
        },
        {
          "number": "9.2",
          "id": "task-9-2",
          "title": "Clone and stage the Orange SSH block rule",
          "href": "lab-09.html#task-9-2"
        },
        {
          "number": "9.3",
          "id": "task-9-3",
          "title": "Activate Orange, verify SSH blocking, restore Green",
          "href": "lab-09.html#task-9-3"
        }
      ],
      "explainers": [
        {
          "id": "ransomware-kill-switch-context",
          "title": "Ransomware Kill Switch: why and how",
          "href": "lab-09.html#ransomware-kill-switch-context",
          "keywords": "incident containment green orange SSH lateral movement emergency isolation"
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
      "label": "Ransomware Kill Switch",
      "href": "lab-09.html#ransomware-kill-switch-context",
      "keywords": "incident containment Orange Green tiered SSH policy"
    }
  ]
};
