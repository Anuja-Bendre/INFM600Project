pragma solidity >=0.7.0 <0.9.0; // Versions of the compiler that can be used to compile the contract
contract DataGovernance{ // Defination of the smart contract
    address public owner; // The account of the owner of data
    mapping (address => bool) isSeeker; // mapping variable that stores a key value pair (maps the boolean value for is Seeker corresponding to each address)

    // address public seeker; // The account of the seeker requesting access to the data
    bytes32 secret = "uniqueaccesscode"; // The secret message shared to the subscribers of the contract
    string accesslink = "contentidentifier";// Link to the data (CID - multihash of the file/document/webpage)

    // Constructor code is only run when the contract
    // is created
    constructor() {
        owner = msg.sender;
    }


    // Allows the owner of the contract to add the public address of a seeker
    // That the owner wishes to grant access for the data
    function addAccess(address seeker) public returns (address){
        require(msg.sender == owner, "Must be Owner of the Contract");
        require(!isSeeker[seeker]);
        isSeeker[seeker] = true;
        return seeker;
    }

    // Allows the seeker to access the data via the link/content_identifier to the data owned by the owner
    function accessData(bytes32 secret, bytes memory signature) public view returns (string memory){
        // bytes32 message = prefixed(keccak256(abi.encodePacked(msg.sender, secret)));
        require(isSeeker[recoverSigner(secret, signature)] == true, "Is not authorised to access the data!");
        return accesslink;
    }

    // Recovers the public address of the account used to sign the message
    function recoverSigner(bytes32 message, bytes memory sig) private pure returns (address)
    {
       uint8 v;
       bytes32 r;
       bytes32 s;

       (v, r, s) = splitSignature(sig);
       return ecrecover(message, v, r, s);
  }

  // Splits the signature to retireve the indivdual componenets
  function splitSignature(bytes memory sig) private pure returns (uint8, bytes32, bytes32){
       require(sig.length == 65);
       
       bytes32 r;
       bytes32 s;
       uint8 v;

       assembly {
           // first 32 bytes, after the length prefix
           r := mload(add(sig, 32))
           // second 32 bytes
           s := mload(add(sig, 64))
           // final byte (first byte of the next 32 bytes)
           v := byte(0, mload(add(sig, 96)))
       }

       return (v, r, s);
   }
}