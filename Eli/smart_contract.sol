pragma solidity ^0.5.0;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC721/ERC721Full.sol";

contract CarRegistry is ERC721Full {
    constructor() public ERC721Full("ArtRegistryToken", "ART") {}

    struct QRCode {
        string name;
        string vin;
        string url;
    }

    mapping(uint256 => QRCode) public vehicleCollection;
    
    function registerCar(
        address owner,
        string memory name,
        string memory vin,
        string memory url
    ) public returns (uint256) {
        uint256 tokenId = totalSupply();

        _mint(owner, tokenId);
        _setTokenURI(tokenId, url);

        vehicleCollection[tokenId] = QRCode(name, vin, url);

        return tokenId;
    }


    }