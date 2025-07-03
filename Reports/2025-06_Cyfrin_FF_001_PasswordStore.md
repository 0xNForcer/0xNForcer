# Formal Verification Report: PasswordStore - Cyfrin First Flight #1
- Contest: https://codehawks.cyfrin.io/c/2023-10-PasswordStore
- Repository: https://github.com/Cyfrin/2023-10-PasswordStore
- Commit: cbf6c9
- Date: June 2025
- Author: [@0xNForcer](https://x.com/0xNForcer)
- [Certora Repo](https://github.com/0xNForcer/0xNForcer/tree/main/Certora/Cyfrin/FirstFlights/01_PasswordStore/certora)

# About 0xNForcer

I provide formal verification services for smart contracts using Certora Prover, focusing on auditing DeFi and blockchain protocols. I thoroughly verify critical properties and invariants to identify and reduce issues before deployment.

Reach out if you're looking to strengthen your project's security through formal verification. Check out my work [here](https://github.com/0xNForcer/0xNForcer) or reach out on [@0xNForcer](https://x.com/0xNForcer).

# Protocol Summary

The PasswordStore smart contract is designed as a simple password management system that allows a single owner to store and retrieve a private password.

# Disclaimer

A smart contract security review, including formal verification, cannot guarantee your contracts are completely free of vulnerabilities. While we strive to identify as many issues as possible, no process ensures 100% security. We strongly recommend ongoing audits, bug bounty programs, formal verification, and continuous on-chain monitoring.

# Table of Contents
- [Formal Verification Report: PasswordStore - Cyfrin First Flight #1](#formal-verification-report-passwordstore---cyfrin-first-flight-1)
- [About 0xNForcer](#about-0xnforcer)
- [Protocol Summary](#protocol-summary)
- [Disclaimer](#disclaimer)
- [Table of Contents](#table-of-contents)
- [Formal Verification Methodology](#formal-verification-methodology)
  - [Types of Properties](#types-of-properties)
- [Verification Results](#verification-results)
  - [Access Control](#access-control)
- [Risk Classification](#risk-classification)
- [Findings](#findings)
- [High](#high)
  - [H-01 - Anyone Can Change Owner's Password due to Missing Check](#h-01---anyone-can-change-owners-password-due-to-missing-check)



# Formal Verification Methodology

Certora Formal Verification mathematically proves smart contract correctness by checking code against specified rules. Unlike testing or fuzzing, which rely on predefined cases, formal verification analyzes all possible contract states and execution paths.

## Types of Properties

**Invariants:**

- Conditions that must always remain true.
- Example: "Total supply always equals sum of balances."

**Rules:**

- Specific behavioral checks or conditions.
- Example: "Withdrawal decreases user's balance."

**Rules typically include:**

- Setup assumptions
- Function executions
- Assertions (conditions always true)

# Verification Results

## Access Control
<table style="width: 100%; table-layout: fixed;">
  <thead>
    <tr>
      <th style="width: 10%;">Source</th>
      <th style="width: 20%;">Rule Name</th>
      <th style="width: 60%;">Description</th>
      <th style="width: 10%;">Report</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>AC_01</td>
      <td>only_the_owner_can_set_new_password</td>
      <td>only the owner should be able to set a new password</td>
      <td><a href="https://prover.certora.com/output/6054208/5138f066b3ee41b7895b2677a14d4376?anonymousKey=5af5fdc599ea479d1fd7158cad9f480ff5940983" target="_blank">❌</a></td>
    </tr>
    <tr>
      <td>AC_02</td>
      <td>only_the_owner_should_be_able_to_view_password</td>
      <td>only the owner should be able to view the password</td>
      <td><a href="https://prover.certora.com/
output/6054208/679cb13fd9b14301a2089737a1d8753a?anonymousKey=3c4aca85c583191d637ad5719033ac745f548ecb" target="_blank">✅</a></td>
    </tr>
    <tr>
      <td>AC_03</td>
      <td>owner_should_never_change</td>
      <td>owner should never be able to change</td>
      <td><a href="https://prover.certora.com/output/6054208/
69bd75a0ba0c4b419ff6ef0daa52e41e?anonymousKey=1d0781c6eddb57d84bee555b70e9dcb6504e749d" target="_blank">✅</a></td>
    </tr>
    <tr>
      <td>AC_04</td>
      <td>only_setPassword_can_change_password</td>
      <td>only `setPassword` can change the password</td>
      <td><a href="https://prover.certora.com/output/6054208/
6f68d3ac190f4f159842569c968c1c11?anonymousKey=fe5f3461cd4365c8dc9099b793c1d1179813212f" target="_blank">✅</a></td>
    </tr>    
  </tbody>
</table>

# Risk Classification
 
| Severity               | Impact: High | Impact: Medium | Impact: Low |
| ---------------------- | ------------ | -------------- | ----------- |
| **Likelihood: High**   | High         | High           | Medium      |
| **Likelihood: Medium** | High         | Medium         | Low         |
| **Likelihood: Low**    | Medium       | Low            | Low         |

<!-- # Audit Details 
## Scope 
## Roles
# Executive Summary
## Issues found -->
# Findings
# High
## H-01 - Anyone Can Change Owner's Password due to Missing Check
### Summary
The `setPassword()` function has no restriction, letting any user overwrite the owner's secret password.

### Description
The `setPassword()` method doesn't verify if the caller is the owner. This means anyone can:
- Call `setPassword()` and set any new password.
- Immediately overwrite the owner's existing secret.

This flaw undermines the fundamental security assumption that only the owner can modify private data. The issue can be exploited instantly with a single transaction and does not require any special conditions.
### Impact
**High** – Allows anyone to alter sensitive data, compromising confidentiality and the trustworthiness of the stored password.
### Likelihood
**High** – Since the function is publicly accessible without any checks.
### Proof of Concept

Here are the logs:
```bash
Logs:
  Owner: 0x1804c8AB1F12E6bbf3894d4083f33e07309d1f38
  Original password: owner_password
  Attacker (not owner): 0x0000000000000000000000000000000000000001
  Password after attack: attacker_password
  Attack successful: Non-owner changed owner's password
```

and the test:
``` solidity
    function test_anyone_can_set_password() public {
        console.log("Owner:", owner);
        
        // Owner sets initial password
        vm.startPrank(owner);
        passwordStore.setPassword("owner_password");
        console.log("Original password:", passwordStore.getPassword());
        vm.stopPrank();
        
        // Attacker changes password (this should fail but doesn't!)
        vm.startPrank(address(1));
        console.log("Attacker (not owner):", address(1));
        
        string memory attackerPassword = "attacker_password";
        passwordStore.setPassword(attackerPassword);  // This succeeds - BUG!
        vm.stopPrank();
        
        // Owner checks password and finds it changed
        vm.startPrank(owner);
        string memory currentPassword = passwordStore.getPassword();
        console.log("Password after attack:", currentPassword);
        console.log("Attack successful: Non-owner changed owner's password");
        
        // Verify the password was actually changed
        assertEq(currentPassword, attackerPassword);
    }
```

### Recommendation

Ensure only the owner can update the password by adding a simple ownership check:
```solidity
    function setPassword(string memory newPassword) external {
        if (msg.sender != s_owner) {
            revert PasswordStore__NotOwner();
        }
        s_password = newPassword;
        emit SetNetPassword();
    }
```
