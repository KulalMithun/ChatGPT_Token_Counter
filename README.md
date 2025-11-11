# ChatGPT_Token_Counter

<h1 align="center">🧠 ChatGPT Token Usage Analyzer</h1>

<p align="center">
  <b>A Simple Python tool to analyze your ChatGPT export and calculate token usage per model, including top chats and cost estimation.</b>
</p>

<hr>

<h3>A Star is Appreciated 🤝</h3>

<h2>📜 Overview</h2>

<p>
This script scans your exported ChatGPT conversation data (<code>conversations.json</code>) and generates a detailed token usage report. 
It detects which models were used (<code>gpt-3.5</code>, <code>gpt-4</code>, etc.), counts total tokens per model, and lists your 
top 10 longest chats by token count. You can also optionally estimate your approximate usage cost.
</p>

<hr>

<h2>🚀 Features</h2>

<ul>
  <li>🔍 Automatically detects all models used in your ChatGPT export.</li>
  <li>📊 Calculates total chats, total messages, and total tokens per model.</li>
  <li>💰 Optional cost estimation based on model pricing (configurable).</li>
  <li>🏆 Lists your top 10 longest chats by token usage.</li>
  <li>⚡ Fast processing with progress bars using <code>tqdm</code>.</li>
  <li>💬 Handles message content extraction safely and recursively.</li>
</ul>

<hr>

<hr>

<h2>🧩 Requirements</h2>

<p>Go to ChatGPT -> Profile -> Data Control -> Export Data(you'll get your chatgpt data within 5-10 Mins)</p>

<p>Install the following dependencies:</p>

<pre><code>pip install tiktoken tqdm</code></pre>

<hr>

<h2>⚙️ Usage</h2>

<p>Run the script from your terminal or command prompt:</p>

<pre><code>python ChatGPT.py </code></pre>

<hr>

<h2>📄 Example Output</h2>

<pre>
🔍 Reading conversations.json ...
Detected models: gpt-4-turbo, gpt-3.5-turbo

Processing chats for gpt-4-turbo: 100%|█████████████████████| 120/120 [00:02<00:00, 42.11it/s]

=== Token Usage Report (per model) ===

Model: gpt-4-turbo
  Total chats processed: 120
  Total messages processed: 2,453
  Total tokens used: 678,432
  Estimated cost (approx): $3.39
  Top 10 longest chats by tokens:
    1. ML Project Guidance — 42,312 tokens, 56 messages
    2. Resume Optimization — 31,104 tokens, 38 messages
    ...
</pre>

<hr>


<h2>🧰 Example Integration</h2>

<p>
You can easily integrate this script into a Jupyter Notebook, 
or modify it to save the results as CSV or JSON for data analysis.
</p>

<hr>

<h2>📄 License</h2>

<p>
MIT License – free to use, modify, and distribute.
</p>

<hr>

<h4>ToDo : </h4>
<p>Any Contribution are Welcome</p>

<h2>👨‍💻 Author : </h2>

<p>
Developed by <b>Mithun </b> – <br>
💬 Passionate about AI, Python, and automation.
</p>

<hr>

<h2>⭐ Contribute</h2>

<p>
Found a bug or want a feature? Feel free to open a pull request or issue on your GitHub repository.
</p>
