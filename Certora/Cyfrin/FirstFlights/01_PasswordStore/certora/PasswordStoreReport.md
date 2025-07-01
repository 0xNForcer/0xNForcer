# Formal Verification Report: PasswordStore

**Competition:** [First Flight #1: PasswordStore](https://codehawks.cyfrin.io/c/2023-10-PasswordStore)  
**Repository:** https://github.com/Cyfrin/2023-10-PasswordStore  
**Latest Commit Hash:** `bcdf28424d31ad44bd2ec3f8c5c019e71d5c44f4`  
**Date:** June 2025  
**Author:** [@0xNForcer](https://x.com/0xNForcer)  
**Certora Prover Version:** 7.31.0

---

## Protocol Summary

The PasswordStore smart contract is designed as a simple password management system that allows a single owner to store and retrieve a private password.

---

## Formal Verification Methodology

Certora Formal Verification mathematically proves smart contract correctness by checking code against specified rules. Unlike testing or fuzzing, which rely on predefined cases, formal verification analyzes all possible contract states and execution paths.

### Types of Properties

**Invariants:**
- Conditions that must always remain true.
- Example: "Total supply always equals sum of balances."

**Rules:**
- Specific behavioral checks or conditions.
- Example: "Withdrawal decreases user's balance."

Rules typically include:
- Setup assumptions
- Function executions
- Assertions (conditions always true)

---

## Verification Results

|Rule Name|Status|Description|Report|Issue|
|---|---|---|---|---|
|only_the_owner_can_set_new_password|❌ Violated|only the owner should be able to set a new password|[Report](https://prover.certora.com/output/6054208/5138f066b3ee41b7895b2677a14d4376?anonymousKey=5af5fdc599ea479d1fd7158cad9f480ff5940983)||
|only_the_owner_should_be_able_to_view_password|✅ Passed|only the owner should be able to view the password|[Report](https://prover.certora.com/output/6054208/679cb13fd9b14301a2089737a1d8753a?anonymousKey=3c4aca85c583191d637ad5719033ac745f548ecb)||
|owner_should_never_change|✅ Passed|owner should never be able to change|[Report](https://prover.certora.com/output/6054208/69bd75a0ba0c4b419ff6ef0daa52e41e?anonymousKey=1d0781c6eddb57d84bee555b70e9dcb6504e749d)||
|only_setPassword_can_change_password|✅ Passed|only setPassword can change the password|[Report](https://prover.certora.com/output/6054208/6f68d3ac190f4f159842569c968c1c11?anonymousKey=fe5f3461cd4365c8dc9099b793c1d1179813212f)||

---

## Disclaimer

This report is provided for informational purposes only and does not constitute a guarantee of contract security. While formal verification significantly enhances confidence in smart contract behavior, it cannot assure absolute security against all possible threats. 0xNForcer and associated entities disclaim all warranties, explicit or implied, regarding the information and results presented herein, and shall not be liable for any claims, damages, or other liabilities arising from the use or interpretation of this report.