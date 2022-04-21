// Take note ID we passed, take note endpoint, after gets response
// reload window

function deleteNote(noteId) {
   fetch('/delete-note', {
      method: 'POST',
      body: JSON.stringify({ noteId: noteId})
   }).then((_res) => {
      // reload window/redirect to homepage
      window.location.href ="/";
   })
}