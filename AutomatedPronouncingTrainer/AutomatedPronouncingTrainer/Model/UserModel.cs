using AutomatedPronouncingTrainer.Service;
using Newtonsoft.Json;

namespace AutomatedPronouncingTrainer.Model
{
    public class UserModel
    {
        [JsonProperty("user_score")]
        public int Score { get; private set; } = 0;

        [JsonProperty("user_level")]
        public UserLevel Level { get; private set; } = UserLevel.B1;
    }
}
