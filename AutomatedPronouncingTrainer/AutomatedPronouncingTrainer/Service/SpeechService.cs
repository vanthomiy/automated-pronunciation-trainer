﻿using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;
using AutomatedPronouncingTrainer.Model;
using Microsoft.AspNetCore.Http;
using Newtonsoft.Json;

namespace AutomatedPronouncingTrainer.Service
{
    public class SpeechService
    {
        private readonly HttpClient httpClient;
        private const string baseUrl = "http://localhost:5000/api/";

        public SpeechService(HttpClient httpClient)
        {
            this.httpClient = httpClient;
        }

        public async Task<bool> LoginAsync(string username)
        {
            var response = await httpClient.GetAsync(baseUrl + "login/" + username);
            var content = await response.Content.ReadAsStringAsync();

            return content == "true";
        }

        public async Task<byte[]> SetNoise(string noise)
        {
            var response = await httpClient.GetAsync(baseUrl + "set_noise/" + noise);
            var content = await response.Content.ReadAsByteArrayAsync();

            return content;
        }

        public async Task<bool> SetModel(string model)
        {
            var response = await httpClient.GetAsync(baseUrl + "set_model/" + model);
            var content = await response.Content.ReadAsStringAsync();

            return content == "true";
        }

        public async Task<List<string>> GetAvailableNoise()
        {
            var response = await httpClient.GetAsync(baseUrl + "noise");
            var content = await response.Content.ReadAsStringAsync();
            var models = JsonConvert.DeserializeObject<List<string>>(content);
            return models;
        }

        public async Task<bool> ChangeLevel(int index)
        {
            var response = await httpClient.GetAsync(baseUrl + "user/change_level/" + index);
            var content = await response.Content.ReadAsStringAsync();

            return content == "true";
        }

        public async Task<List<string>> GetAvailableModels()
        {
            var response = await httpClient.GetAsync(baseUrl + "models");
            var content = await response.Content.ReadAsStringAsync();
            var models = JsonConvert.DeserializeObject<List<string>>(content);
            return models;
        }

        /// <summary>
        /// Send record as byte array to server
        /// </summary>
        /// <param name="file"></param>
        /// <returns></returns>
        public async Task<RecordingResult?> SendRecordAsync(byte[] file)
        {
            var response = await httpClient.PostAsync(baseUrl + "send_record", new ByteArrayContent(file));
            var content = await response.Content.ReadFromJsonAsync<RecordingResult>();

            return content;
        }

        /// <summary>
        /// Get the byte array of the record with noise
        /// </summary>
        /// <returns></returns>
        public async Task<byte[]> GetRecordNoise()
        {
            var response = await httpClient.GetAsync(baseUrl + "get_record");
            var content = await response.Content.ReadAsByteArrayAsync();

            return content;
        }

        public async Task<string> GetNextAsync()
        {
            var response = await httpClient.GetAsync(baseUrl + "next");
            var content = await response.Content.ReadAsStringAsync();
            return content;
        }

        public async Task<List<ResultHistory>> GetUserHistoryAsync()
        {
            var response = await httpClient.GetAsync(baseUrl + "history");
            var content = await response.Content.ReadAsStringAsync();
            var history = JsonConvert.DeserializeObject<List<ResultHistory>>(content);
            return history;
        }

        public async Task<UserModel> GetUserAsync()
        {
            var response = await httpClient.GetAsync(baseUrl + "user");
            var content = await response.Content.ReadAsStringAsync();
            var user = JsonConvert.DeserializeObject<UserModel>(content);
            return user;
        }
    }

    public class RecordingResult
    {

        [JsonProperty("text")]
        public string Text { get; set; }

        [JsonProperty("score")]
        public double Score { get; set; }

        [JsonProperty("data")]
        public byte[]? Data { get; set; }
    }
}
