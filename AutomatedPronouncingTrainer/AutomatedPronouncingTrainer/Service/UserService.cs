using AutomatedPronouncingTrainer.Model;

namespace AutomatedPronouncingTrainer.Service
{
    public class UserService
    {
        public bool IsLoggedIn { get; set; } = false;
        public string CurrentModel { get; set; } = "base.en";
        public string CurrentNoise { get; set; } = "None";

        public string UserName { get; set; } = "User";
        public List<ResultHistory> History { get; set; } = new List<ResultHistory>();

        public UserModel User { get; set; } = new UserModel();

    }



    public enum UserLevel
    {
        A1,
        A2,
        B1,
        B2,
        C1,
        C2,
        Nativ
    }
}
