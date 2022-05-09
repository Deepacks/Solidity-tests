// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

// import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "../interfaces/AggregatorV3Interface.sol";
// import "@openzeppelin/contracts/access/Ownable.sol";
import "./openzeppelin/Ownable.sol";
// import "@chainlink/contracts/src/v0.8/VRFConsumerBaseV2.sol";
import "./smartcontractkit/VRFConsumerBaseV2.sol";
// import "@chainlink/contracts/src/v0.8/interfaces/VRFCoordinatorV2Interface.sol";
import "../interfaces/VRFCoordinatorV2Interface.sol";

contract Lottery is VRFConsumerBaseV2, Ownable {
    AggregatorV3Interface internal ethUsdPriceFeed;
    VRFCoordinatorV2Interface COORDINATOR;

    address payable[] public players;
    address payable public recentWinner;
    uint256 public lastRandomness;
    uint256 public usdEntryFee;
    enum LOTTERY_STATE {
        OPEN,
        CLOSED,
        CALCULATING_WINNER
    }
    LOTTERY_STATE public lottery_state;

    uint64 s_subscriptionId;
    bytes32 keyHash;
    uint32 callbackGasLimit;
    uint16 requestConfirmations = 3;
    uint32 numWords = 1;
    uint256[] public s_randomWords;

    constructor(
        address _priceFeedAddress,
        address _vrfCoordinator,
        uint32 _callbackGasLimit,
        bytes32 _keyhash,
        uint64 _subscriptionId
    ) VRFConsumerBaseV2(_vrfCoordinator) {
        ethUsdPriceFeed = AggregatorV3Interface(_priceFeedAddress);
        COORDINATOR = VRFCoordinatorV2Interface(_vrfCoordinator);

        usdEntryFee = 50 * (10**18);
        lottery_state = LOTTERY_STATE.CLOSED;

        s_subscriptionId = _subscriptionId;
        callbackGasLimit = _callbackGasLimit;
        keyHash = _keyhash;
    }

    function requestRandomness()
        internal
        onlyOwner
        returns (uint256 requestId)
    {
        uint256 s_requestId = COORDINATOR.requestRandomWords(
            keyHash,
            s_subscriptionId,
            requestConfirmations,
            callbackGasLimit,
            numWords
        );
        return s_requestId;
    }

    function getEntranceFee() public view returns (uint256) {
        (, int256 answer, , , ) = ethUsdPriceFeed.latestRoundData();
        return (usdEntryFee * (10**18)) / (uint256(answer) * (10**10));
    }

    function enter() public payable {
        require(lottery_state == LOTTERY_STATE.OPEN, "Lottery is not open");
        require(msg.value >= getEntranceFee(), "Minimum amount not reached");
        players.push(payable(msg.sender));
    }

    function startLottery() public onlyOwner {
        require(lottery_state == LOTTERY_STATE.CLOSED, "Lottery is not closed");
        lottery_state = LOTTERY_STATE.OPEN;
    }

    function endLottery() public onlyOwner {
        lottery_state = LOTTERY_STATE.CALCULATING_WINNER;
        uint256 requestId = requestRandomness();
    }

    function fulfillRandomWords(
        uint256 _requestId,
        uint256[] memory _randomness
    ) internal override {
        require(
            lottery_state == LOTTERY_STATE.CALCULATING_WINNER,
            "Wrong callback call"
        );
        require(_randomness[0] > 0, "Invalid random value");

        uint256 indexOfWinners = _randomness[0] % players.length;
        recentWinner = players[indexOfWinners];
        recentWinner.transfer(address(this).balance);

        players = new address payable[](0);
        lottery_state = LOTTERY_STATE.CLOSED;
        lastRandomness = _randomness[0];
    }
}
