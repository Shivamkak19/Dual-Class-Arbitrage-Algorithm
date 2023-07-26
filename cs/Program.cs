using System;
using Alpaca.Markets;
using System.Threading.Tasks;

namespace AlpacaExample
{

    internal static class Program
    {
            // API Authorization Information
        private const string key_live = "AK0ZSFQIKNH51OYVKMB2";
        private const string key_paper = "PK1VV2Q66XEYIKECOX7Q";
        private const string secret_live = "h6IJcWc4cK8aWBaeIAc4budigRtqSMvxOyq2J2mB";
        private const string secret_paper = "G2DThPl44znonvTQ3SpUUugy9ODapUQZ1aj3gVVp";

        // Toggle Between Live and Paper 
        private const bool live_status = true;

        public static async Task Main()
        {

            var clientLive = Environments.Live
                    .GetAlpacaTradingClient(new SecretKey(key_live, secret_live));
            var clientPaper = Environments.Paper
                    .GetAlpacaTradingClient(new SecretKey(key_paper, secret_paper));

            // Set client based on toggle
            // Manual for now
            var client = clientPaper;  


            var account = await client.GetAccountAsync();
            // Check if our account is restricted from trading.
            if (account.IsTradingBlocked)
            {
                Console.WriteLine("Account is currently restricted from trading.");
            }
            Console.WriteLine(account.BuyingPower + " is available as buying power.");
            Console.Read();
        }
    }
}