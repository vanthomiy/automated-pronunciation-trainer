using AutomatedPronouncingTrainer.Service;
using Newtonsoft.Json;

namespace AutomatedPronouncingTrainer.Model
{
    public class ResultHistory
    {
        [JsonProperty("real_text")]
        public string RealText { get; set; }

        [JsonProperty("spoken_text")]
        public string SpokenText { get; set; }

        [JsonProperty("sentence_score")]
        public int SentenceScore { get; set; }

        [JsonProperty("user_score")]
        public int UserScore { get; set; }

        [JsonProperty("user_level")]
        public UserLevel Level { get; set; }


        /// <summary>
        /// Returns the user level based on the user score
        /// </summary>
        /// <param name="level"></param>
        /// <returns></returns>
        public static int CountFromUserLevel(UserLevel level)
        {
            switch (level)
            {
                case UserLevel.A1:
                    return 0;
                case UserLevel.A2:
                    return 1;
                case UserLevel.B1:
                    return 2;
                case UserLevel.B2:
                    return 3;
                case UserLevel.C1:
                    return 4;
                case UserLevel.C2:
                    return 5;
                case UserLevel.Nativ:
                    return 6;
                default:
                    return 0;
            }
        }
    }
}
