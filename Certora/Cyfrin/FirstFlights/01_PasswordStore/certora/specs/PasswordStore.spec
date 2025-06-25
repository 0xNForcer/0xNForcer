
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


rule sanityCheck {
    method f;
    env e;
    calldataarg args;

    f(e, args);

    assert true;
    satisfy true;
}



// only the owner should be able to set a new password
rule onlyTheOwnerCanSetNewPassword() {
    env e;

    address owner;
    string password;

    bytes32 passwordBefore = ghost_password;

    setPassword(e, password);

    bytes32 passwordAfter = ghost_password;

    assert passwordAfter != passwordBefore => owner == e.msg.sender;
}

//only the owner should be able to view the password
rule onlyTheOwnerShouldBeAbleToViewPassword() {
    env e;

    getPassword@withrevert(e);
    bool didRevert = lastReverted;

    assert !didRevert => e.msg.sender == ghost_owner;
}

//owner should never be able to change
rule ownerShouldNeverChange() {
    env e;
    method f;
    calldataarg args;

    address ownerBefore = ghost_owner;

    f(e, args);

    address ownerAfter = ghost_owner;

    assert ownerBefore == ownerAfter;

}

//only setPassword can change the password
rule only_setPassword_canChangePassword() {
    env e;
    method f;
    calldataarg args;

    bytes32 passwordBefore = ghost_password;

    f(e, args);

    bytes32 passwordAfter = ghost_password;

    assert passwordBefore != passwordAfter => f.selector == sig:setPassword(string).selector;
}

//when password is updated it should be updated to the correct value
rule passwordUpdatedToCorrectValue() {
    env e;

    address owner;
    string password;
    bytes32 passwordhash = keccak256("password");
    // require keccak256(password) == passwordhash;
    require keccak256(password) == to_bytes32(0x5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8); 

    bytes32 passwordBefore = ghost_password;

    setPassword(e, password);

    bytes32 passwordAfter = ghost_password;

    assert passwordAfter == passwordBefore;
}