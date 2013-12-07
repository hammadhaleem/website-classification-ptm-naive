python process.py
for f in *.zip; do
  dir=${f%.zip}

  unzip -d "./$dir" "./$f"
done
rm *.zip
