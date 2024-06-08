from collections import UserDict

class Note(UserDict):
    def add(self, note_title, note_text):

        self.data[note_title] = note_text
        return self.print_single_note(note_title)

    def search(self, request):
        results = []
        for title, text in self.data.items():
            if request in title or request in text:
                results.append((title, text))
        return results

    def edit(self, note_title, new_text):
        if note_title in self.data:
            self.data[note_title] = new_text
            return self.print_single_note(note_title)
        return False

    def delete(self, note_title):
        if note_title in self.data:
            del self.data[note_title]
            return 'Note has been deleted'
        return False

    def print_single_note(self, note_title):
        if note_title in self.data:
            return f"Title: {note_title}\nText: {self.data[note_title]}"
        else:
            return f"Note '{note_title}' not found."

    def print_all_notes(self):
        if not self.data:
            return "\n  No notes available.\n"
        else:
            result = '\n   All notes:\n\n'
            for title, text in self.data.items():
                result += f'  {title.title()}: {text}\n'
            return result
