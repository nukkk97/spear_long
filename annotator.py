import gradio as gr
import csv
import os
import random

# 檔案與資料路徑
CSV_FILE = "/tmp2/b10902112/audio_speech_generate/emotion_tts_assigned_by_distribution.csv"
AUDIO_DIR = "/tmp2/b10902112/audio_speech_generate/pairwise_outputs"
ANNOTATION_FILE = "annotations.csv"

def load_samples():
    samples = []
    with open(CSV_FILE, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            samples.append(row)
    return samples

def load_existing_annotations():
    annotated_ids = set()
    if os.path.exists(ANNOTATION_FILE):
        with open(ANNOTATION_FILE, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                annotated_ids.add(row["id"])
    return annotated_ids

def get_unlabeled_samples():
    all_samples = load_samples()
    annotated_ids = load_existing_annotations()
    remaining = [s for s in all_samples if s["id"] not in annotated_ids]
    return remaining

def get_random_unlabeled_sample():
    remaining = get_unlabeled_samples()
    return random.choice(remaining) if remaining else None

def save_annotation(sample_id, text, preference):
    file_exists = os.path.exists(ANNOTATION_FILE)
    with open(ANNOTATION_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "text", "preference"])
        if not file_exists:
            writer.writeheader()
        writer.writerow({
            "id": sample_id,
            "text": text,
            "preference": preference
        })

def load_ui_from_sample(sample):
    sample_id = sample["id"]
    text = sample["text"]
    emotion = sample["emotions"]
    tts_1 = sample["tts_1"]
    tts_2 = sample["tts_2"]

    audio_1_path = os.path.join(AUDIO_DIR, sample_id, f"{tts_1}.wav")
    audio_2_path = os.path.join(AUDIO_DIR, sample_id, f"{tts_2}.wav")

    prompt = f'Which speech expresses **"{emotion}"** more clearly?'

    return (
        gr.update(visible=True),
        text,
        prompt,
        tts_1,
        audio_1_path,
        tts_2,
        audio_2_path,
        sample_id,
        text,
        gr.update(visible=False)
    )

def submit(choice, sample_id, text, tts1, tts2):
    preference = {
        "System 1": tts1,
        "System 2": tts2
    }.get(choice, "Undecided")

    save_annotation(sample_id, text, preference)
    next_sample = get_random_unlabeled_sample()
    if not next_sample:
        return (
            gr.update(visible=False),  # submit
            "All samples have been annotated!",
            "", "", "", None, "", None, "", "",
            gr.update(value="✅ ALL DATA ARE ANNOTATED.", visible=True)
        )
    return load_ui_from_sample(next_sample)

def load_next_sample():
    sample = get_random_unlabeled_sample()
    if not sample:
        return (
            gr.update(visible=False),  # submit
            "All samples have been annotated!",
            "", "", "", None, "", None, "", "",
            gr.update(value="✅ ALL DATA ARE ANNOTATED.", visible=True)
        )
    return load_ui_from_sample(sample)

with gr.Blocks() as demo:
    gr.Markdown("## 🎧 Emotion Preference Annotation for TTS")
    sample_id_state = gr.State()
    sample_text_state = gr.State()
    status_msg = gr.Markdown(value="", visible=False)

    load_btn = gr.Button("🔁 Load Next Sample")

    text_out = gr.Textbox(label="Text", interactive=False)
    prompt_md = gr.Markdown()

    with gr.Row():
        with gr.Column():
            sys1_label = gr.Text(label="System 1", visible=False)
            audio1_player = gr.Audio(label="Audio 1", type="filepath")
        with gr.Column():
            sys2_label = gr.Text(label="System 2", visible=False)
            audio2_player = gr.Audio(label="Audio 2", type="filepath")

    choice = gr.Radio(choices=["System 1", "System 2"], label="Which system performs better?")
    submit_btn = gr.Button("Submit", visible=False)

    # Load next sample button
    load_btn.click(
        fn=load_next_sample,
        outputs=[
            submit_btn,
            text_out,
            prompt_md,
            sys1_label,
            audio1_player,
            sys2_label,
            audio2_player,
            sample_id_state,
            sample_text_state,
            status_msg
        ]
    )

    # Submit button action
    submit_btn.click(
        fn=submit,
        inputs=[choice, sample_id_state, sample_text_state, sys1_label, sys2_label],
        outputs=[
            submit_btn,
            text_out,
            prompt_md,
            sys1_label,
            audio1_player,
            sys2_label,
            audio2_player,
            sample_id_state,
            sample_text_state,
            status_msg
        ]
    )

demo.launch(share=True)