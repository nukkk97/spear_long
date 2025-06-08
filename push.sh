for d in tts_outputs/urlsf_subset00-*; do
  git add "$d"
  git commit -m "Add $d"
  git push origin main
done