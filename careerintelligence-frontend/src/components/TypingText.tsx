
import { useEffect, useState } from "react";
import "./TypingText.css";

const phrases = [
  "career pathway.",
  "professional future.",
  "dream career.",
  "successful journey.",
];

export default function TypingText() {
  const [text, setText] = useState("");
  const [phraseIndex, setPhraseIndex] = useState(0);
  const [deleting, setDeleting] = useState(false);

  useEffect(() => {
    const currentPhrase = phrases[phraseIndex];

    let delay = deleting ? 45 : 90;

    if (!deleting && text === currentPhrase) {
      delay = 1500;
    }

    if (deleting && text === "") {
      delay = 300;
    }

    const timer = window.setTimeout(() => {
      if (!deleting && text !== currentPhrase) {
        setText(currentPhrase.slice(0, text.length + 1));
      } else if (!deleting && text === currentPhrase) {
        setDeleting(true);
      } else if (deleting && text !== "") {
        setText(text.slice(0, -1));
      } else {
        setDeleting(false);
        setPhraseIndex((prev) => (prev + 1) % phrases.length);
      }
    }, delay);

    return () => window.clearTimeout(timer);
  }, [text, deleting, phraseIndex]);

  return (
    <span className="typing-text" aria-label={phrases[phraseIndex]}>
      {text}
    </span>
  );
}
