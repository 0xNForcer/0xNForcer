
//////////////////////////////////////////
// Ghost & hooks - s_password
/////////////////////////////////////////
ghost bytes32 ghost_password;

hook Sstore PasswordStoreHarness.(slot 1) bytes32 value {
    ghost_password = value;
}

hook Sload bytes32 value PasswordStoreHarness.(slot 1) {
    require ghost_password == value;
}

//////////////////////////////////////////
// Ghost & hooks - s_owner
/////////////////////////////////////////
ghost address ghost_owner;

hook Sstore s_owner address value {
    ghost_owner = value;
}

hook Sload address value s_owner {
    require ghost_owner == value;
}


rule sanity_check {
    method f;
    env e;
    calldataarg args;

    f(e, args);

    assert true;
    satisfy true;
}



//**Description: only the owner should be able to set a new password**
rule only_the_owner_can_set_new_password() {
    env e;

    address owner;
    string password;

    bytes32 passwordBefore = ghost_password;

    setPassword(e, password);

    bytes32 passwordAfter = ghost_password;

    assert passwordAfter != passwordBefore => owner == e.msg.sender;
}

//**Description: only the owner should be able to view the password**
rule only_the_owner_should_be_able_to_view_password() {
    env e;

    getPassword@withrevert(e);
    bool didRevert = lastReverted;

    assert !didRevert => e.msg.sender == ghost_owner;
}

//**Description: owner should never be able to change**
rule owner_should_never_change() {
    env e;
    method f;
    calldataarg args;

    address ownerBefore = ghost_owner;

    f(e, args);

    address ownerAfter = ghost_owner;

    assert ownerBefore == ownerAfter;

}

//**Description: only setPassword can change the password**
rule only_setPassword_can_change_password() {
    env e;
    method f;
    calldataarg args;

    bytes32 passwordBefore = ghost_password;

    f(e, args);

    bytes32 passwordAfter = ghost_password;

    assert passwordBefore != passwordAfter => f.selector == sig:setPassword(string).selector;
}