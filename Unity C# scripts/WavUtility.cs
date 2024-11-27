using System;
using System.IO;
using UnityEngine;

public static class WavUtility
{
    // Convert an AudioClip to a WAV byte array
    public static byte[] FromAudioClip(AudioClip clip)
    {
        using (MemoryStream stream = new MemoryStream())
        {
            WriteWav(clip, stream);
            return stream.ToArray();
        }
    }

    // Convert a WAV byte array to an AudioClip
    public static AudioClip ToAudioClip(byte[] wavFile)
    {
        using (MemoryStream stream = new MemoryStream(wavFile))
        {
            return ReadWav(stream);
        }
    }

    // Writes an AudioClip to a stream in WAV format
    private static void WriteWav(AudioClip clip, Stream stream)
    {
        int sampleCount = clip.samples * clip.channels;
        int sampleRate = clip.frequency;
        int headerSize = 44; // Standard WAV header size

        // Write WAV header
        using (BinaryWriter writer = new BinaryWriter(stream))
        {
            writer.Write("RIFF".ToCharArray());
            writer.Write(headerSize - 8 + sampleCount * 2); // File size minus RIFF and file size fields
            writer.Write("WAVE".ToCharArray());
            writer.Write("fmt ".ToCharArray());
            writer.Write(16); // Sub-chunk size for PCM
            writer.Write((short)1); // Audio format (PCM)
            writer.Write((short)clip.channels);
            writer.Write(sampleRate);
            writer.Write(sampleRate * 2 * clip.channels); // Byte rate
            writer.Write((short)(clip.channels * 2)); // Block align
            writer.Write((short)16); // Bits per sample

            writer.Write("data".ToCharArray());
            writer.Write(sampleCount * 2); // Data chunk size

            float[] samples = new float[sampleCount];
            clip.GetData(samples, 0);

            // Convert float samples to 16-bit PCM and write to stream
            foreach (var sample in samples)
            {
                short intSample = (short)(sample * 32767);
                writer.Write(intSample);
            }
        }
    }

    // Reads a WAV file from a stream and converts it to an AudioClip
    private static AudioClip ReadWav(Stream stream)
    {
        using (BinaryReader reader = new BinaryReader(stream))
        {
            if (stream.Length < 44)
            {
                Debug.LogError("Invalid WAV file - stream is too short.");
                return null;
            }

            // Read header
            string riff = System.Text.Encoding.ASCII.GetString(reader.ReadBytes(4));
            int fileSize = reader.ReadInt32();
            string wave = System.Text.Encoding.ASCII.GetString(reader.ReadBytes(4));

            if (riff != "RIFF" || wave != "WAVE")
            {
                Debug.LogError("Invalid WAV format - missing RIFF or WAVE headers.");
                return null;
            }

            // Read "fmt " subchunk
            string fmt = System.Text.Encoding.ASCII.GetString(reader.ReadBytes(4));
            int subChunkSize = reader.ReadInt32();
            short audioFormat = reader.ReadInt16();
            int channels = reader.ReadInt16();
            int sampleRate = reader.ReadInt32();
            int byteRate = reader.ReadInt32();
            short blockAlign = reader.ReadInt16();
            short bitsPerSample = reader.ReadInt16();

            if (fmt != "fmt " || audioFormat != 1)
            {
                Debug.LogError("Invalid WAV format - unsupported format or non-PCM data.");
                return null;
            }

            // Read "data" subchunk
            string dataString = System.Text.Encoding.ASCII.GetString(reader.ReadBytes(4));
            int dataSize = reader.ReadInt32();

            Debug.Log($"Channels: {channels}, Sample Rate: {sampleRate}, Data Size: {dataSize}, Byte Rate: {byteRate}, Block Align: {blockAlign}, Bits per Sample: {bitsPerSample}");

            // Ensure data size is valid
            if (dataSize <= 0 || channels <= 0 || sampleRate <= 0)
            {
                Debug.LogError("Invalid WAV file - essential audio parameters are zero.");
                return null;
            }

            // Read audio data
            float[] samples = new float[dataSize / (bitsPerSample / 8)];
            for (int i = 0; i < samples.Length; i++)
            {
                samples[i] = reader.ReadInt16() / 32768f;
            }

            AudioClip clip = AudioClip.Create("GeneratedAudio", samples.Length, channels, sampleRate, false);
            clip.SetData(samples, 0);

            return clip;
        }
    }
}
