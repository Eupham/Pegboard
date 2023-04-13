import json
import re
import requests
import time
import pathlib as path
import glob

output_dir = path.Path("scrape_output")
output_dir.mkdir(exist_ok=True)

 
class RobotParser:
    def __init__(self, url, user_agent):
        self.url = url
        self.user_agent = user_agent
        self.robot_rules = {}
        self.tree = {}
 
    def get_robots_txt(self):
        headers = {"User-Agent": self.user_agent}
        response = requests.get(self.url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            return None
 
    def parse_robots_txt(self, text):
        current_agent = None
        for line in text.split("\n"):
            key, value = self.parse_line(line)
            if key == "User-agent":
                current_agent = value
                self.robot_rules[current_agent] = []
            elif key == "Disallow" and current_agent is not None:
                self.robot_rules[current_agent].append(value)
 
    def store_json(self, filename):
        with open(filename, "w") as f:
            json.dump(self.structure_rules(), f, indent=4)
 
    def structure_rules(self):
        tree = {}
        for agent, disallows in self.robot_rules.items():
            for disallow in disallows:
                parts = disallow.split("/")
                current = tree
                for part in parts:
                    if not part:
                        continue
                    regex_part = re.sub(r"[^a-zA-Z0-9-_]", r"_", part)
                    current = current.setdefault(regex_part, {})
                current["agent"] = agent
        return tree
 
    def parse_line(self, line):
        parts = line.split(":")
        if len(parts) == 2:
            key, value = parts
            return key.strip(), value.strip()
        else:
            return None, None
 
    def is_allowed(self, url):
        for agent, disallows in self.robot_rules.items():
            if agent == "*" or agent == self.user_agent:
                for disallow in disallows:
                    if re.match(disallow, url):
                        return False
        return True
 
    def store_results(self, url, results):
        # Extract the page name from the URL
        page_name = re.findall(r"/wiki/(.*)", url)[0]
 
        sentences = []
 
        sentences_raw = re.findall(r"[^.!?]+[.!?]", results, flags=re.DOTALL)
 
        for i, sentence in enumerate(sentences_raw):
            sentence = re.sub(r"<.*?>", " ", sentence)
 
            sentences.append(sentence.strip())
 
        query = re.sub(r"_", " ", page_name)
        filename = output_dir / f"{query}.json"
        with open(filename, "w") as f:
            json.dump(sentences, f, indent=4)
 
    def main(queries):
        url = "https://en.wikipedia.org/robots.txt"
        user_agent = "WqEtiquette/0.1.4"
 
        parser = RobotParser(url, user_agent)
 
        robot_text = parser.get_robots_txt()
        if robot_text:
            parser.parse_robots_txt(robot_text)
            print("JSON object saved to robot_rules.json")
        else:
            print("Failed to get robots.txt")
 
        for query in queries:
            print(f"Processing query: {query}")
            query_url = query.replace(' ', '_')
            url = f"https://en.wikipedia.org/wiki/{query_url}"
            headers = {"User-Agent": user_agent}
 
            if not parser.is_allowed(url):
                print(f"The URL '{url}' is not allowed to be crawled according to the rules in the robots.txt file.")
                continue
 
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                title = re.findall(r"<title>(.*?) - Wikipedia</title>", response.text)
                redirect = re.findall(r'<a href="/wiki/([^"#]+)"', response.text)
                if title:
                    print(f"Processed query: {query}. Page title: {title[0]}")
                    results = response.text
                    parser.store_results(url, results)
                elif redirect:
                    print(f"Processed query: {query}. Redirecting to: {redirect[0]}")
                else:
                    print(f"Processed query: {query}. No results found.")
 
            else:
                print("Failed to search Wikipedia.")
 
            time.sleep(10)
 
        print("Processing complete.")

class TextProcessor:
    def __init__(self, filenames):
        self.filenames = filenames
        self.text = self.read_files()
        self.words = self.count_words_occurrences()
        self.letters = self.count_letters()
        self.symbols = self.count_symbols()
        self.websites = self.find_websites()
        self.emails = self.find_emails()
        self.word_count = len(re.findall(r'\b\w+\b', self.text))
        self.domains = self.get_domains()
        self.letter_ngrams = self.extract_ngrams(2, self.letters)
        self.symbol_ngrams = self.extract_ngrams(2, self.symbols)
        self.word_ngrams = self.extract_ngrams(3, self.words)
        self.symbol_distances = self.calculate_symbol_distances()

    def extract_ngrams(self, n, data):
        ngrams = {}
        for key in data:
            if len(key) >= n:
                for i in range(len(key)-n+1):
                    ngram = key[i:i+n]
                    if ngram in ngrams:
                        ngrams[ngram].append(data[key])
                    else:
                        ngrams[ngram] = [data[key]]
        return ngrams

    def calculate_symbol_distances(self):
        distances = {}
        for key in self.symbols:
            if len(key) == 1:
                for i in range(len(self.text)):
                    if self.text[i] == key:
                        distances.setdefault(key, []).append(i)
        return distances


    def get_domains(self):
        domains = []
        for website in self.websites:
            domain = website.split('//')[-1].split('/')[0]
            domain = re.sub(r'^www\.', '', domain)  # Remove 'www.' prefix
            tld = re.findall(r'\.([a-z]+)$', domain)
            if tld:
                domains.append(tld[0])
        return domains

    def read_files(self):
        text = ""
        for filename in self.filenames:
            with open(filename, "r") as f:
                text += f.read()
        return text

    def count_words_occurrences(self):
        words_occurrences = {}
        words = re.findall(r'\b\w+\b', self.text)
        for word in words:
            words_occurrences[word] = words_occurrences.get(word, 0) + 1
        return words_occurrences

    def count_letters(self):
        letter_count = {}
        for letter in re.findall(r'[a-zA-Z]', self.text):
            letter_count[letter] = letter_count.get(letter, 0) + 1
        return letter_count

    def count_symbols(self):
        symbol_count = {}
        for symbol in re.findall(r'[^\w\s]', self.text):
            symbol_count[symbol] = symbol_count.get(symbol, 0) + 1
        return symbol_count

    def find_websites(self):
        return re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', self.text)

    def find_emails(self):
        return re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', self.text)

class NgramParser:
    def __init__(self, page_stats):
        self.page_stats = page_stats
        self.letter_ngrams = {}
        self.symbol_ngrams = {}
        self.word_ngrams = {}
 
    def extract_ngrams(self, n):
        self.letter_ngrams = self._get_ngrams(self.page_stats.letters, n)
        print("Letter ngrams:", self.letter_ngrams)
        self.symbol_ngrams = self._get_ngrams(self.page_stats.symbols, n)
        print("Symbol ngrams:", self.symbol_ngrams)
        self.word_ngrams = self._get_ngrams(self.page_stats.word_occurrences, n)
        print("Word ngrams:", self.word_ngrams)

    def _get_ngrams(self, tokens, n):
        ngrams = {}
        for token, pages_counts in tokens.items():
            print("Token:", token)
            print("Pages counts:", pages_counts)
            for i in range(len(pages_counts) - n + 1):
                ngram_pages_counts = pages_counts[i:i+n]
                ngram_key = tuple([(page, count) for page, count in ngram_pages_counts])
                if ngram_key in ngrams:
                    ngrams[ngram_key].append(token)
                else:
                    ngrams[ngram_key] = [token]
        return ngrams

class PageStatsAggregator:
    def __init__(self, directory):
        self.directory = directory
        self.letters = {}
        self.symbols = {}
        self.word_occurrences = {}
        self.total_words = 0

    def aggregate(self):
        # iterate over all _attribute.json files in the directory
        for filename in glob.glob(str(output_dir / "*_attributes.json")):
            with open(filename, "r") as file:
                # load JSON data from the file
                data = json.load(file)

                # get the page name from the file name
                page_name = filename.split("/")[-1].replace("_attributes.json", "")

                # increment total word count by the count of words in the current file
                self.total_words += data["words"]

                # add the letter counts in the current file to the global letter count dictionary
                for letter, count in data["letters"].items():
                    if letter in self.letters:
                        self.letters[letter].append([page_name, count])
                    else:
                        self.letters[letter] = [[page_name, count]]

                # add the symbol counts in the current file to the global symbol count dictionary
                for symbol, count in data["symbols"].items():
                    if symbol in self.symbols:
                        self.symbols[symbol].append([page_name, count])
                    else:
                        self.symbols[symbol] = [[page_name, count]]

                # add the word occurrences in the current file to the global word occurrence dictionary
                for word, count in data["word_occurrences"].items():
                    if word in self.word_occurrences:
                        self.word_occurrences[word].append([page_name, count])
                    else:
                        self.word_occurrences[word] = [[page_name, count]]

        # sort the values in the dictionaries by page name
        for d in [self.letters, self.symbols, self.word_occurrences]:
            for key in d:
                d[key] = sorted(d[key], key=lambda x: x[0])

        # construct the final output dictionary
        output = {
            "words": self.total_words,
            "letters": self.letters,
            "symbols": self.symbols,
            "word_occurrences": self.word_occurrences
        }

        return output

if __name__ == '__main__':
    queries = ["signal processing", "python programming", "bird song"]
    RobotParser.main(queries)
    filenames = [output_dir / f"{q.replace(' ', ' ')}.json" for q in queries]

    # Iterate over the filenames and process each file separately
    for filename in filenames:
        # Create a new TextProcessor object for each file
        text_processor = TextProcessor([filename])

        # Extract the page name from the filename
        page_name = filename.replace('.json', '')

        # Create a dictionary of the attributes for the page
        page_data = {
            'words': text_processor.word_count,
            'letters': text_processor.letters,
            'symbols': text_processor.symbols,
            'word_occurrences': text_processor.count_words_occurrences(),
            'letter_ngrams': text_processor.letter_ngrams,
            'symbol_ngrams': text_processor.symbol_ngrams,
            'word_ngrams': text_processor.word_ngrams
        }

        # Save the dictionary as a JSON file
        with open(output_dir / f"{page_name}_attributes.json", 'w') as f:
            json.dump(page_data, f, indent=4)

    # Aggregate the statistics across all pages and output the results to a separate JSON file
    aggregator = PageStatsAggregator(output_dir)
    aggregated_stats = aggregator.aggregate()
    with open(output_dir / "aggregated_stats.json", "w") as f:
        json.dump(aggregated_stats, f, indent=4)