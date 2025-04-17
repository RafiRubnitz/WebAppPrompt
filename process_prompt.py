"""
This module defines the PromptProcessor class, responsible for generating and refining prompts
based on a given conversation summary using a language model (LLM).

Workflow:
1. Receives a final summary of the conversation.
2. Generates an initial prompt using the LLM.
3. Evaluates the prompt and identifies potential improvements.
4. Refines the prompt based on the feedback.
5. Returns the final version of the prompt to be sent to the user.
"""



class PromptProcessor:
    def __init__(self, llm):
        self.llm = llm
        self.messages = []

    def process_prompt(self, summary):
        """
        Process the final summary and generate a prompt for the LLM.
        """
        # Create a prompt based on the summary
        prompt = self._generate_prompt(summary)
        # Send the prompt to the LLM and get the response
        conclusion = self._over_view_prompt(prompt)
        # Process the response and generate the final prompt
        response = self._generate_final_prompt(conclusion,prompt)
        # Return the final prompt
        return response

    def _generate_prompt(self, summary: str) -> str:
        """
        Generate a prompt for the LLM based on the summary.
        """
        # This is a placeholder for the actual prompt generation logic
        message = (f"Based on the following summary, generate a professional-level prompt that serves as a functional specification document."
                   f" The prompt should be detailed and structured in a way that a developer can use it to implement the described behavior in code"
                   f" without further clarification.\n\n{summary}")

        self.messages.append({"role": "user", "content": message})
        return self.llm.chat(self.messages)

    def _over_view_prompt(self, prompt: str) -> str:
        """
        Generate an overview of the prompt for the LLM.
        """
        # This is a placeholder for the actual overview generation logic
        message = (
            "Review the following functional specification. "
            "List any missing details, unclear instructions, or areas for improvement. "
            "Your goal is to help make this document ready for implementation by a developer.\n\n"
            f"{prompt}"
        )

        self.messages.append({"role": "user", "content": message})

        return self.llm.chat(self.messages)

    def _generate_final_prompt(self, conclusion: str,prompt: str) -> str:
        """
        Generate the final prompt for the LLM based on the response.
        """
        # This is a placeholder for the actual final prompt generation logic
        message = (f"for this prompt:\n\n{prompt}\n"
                   f"And based on the following response, generate a final prompt for the LLM:\n\n{conclusion}")

        self.messages.append({"role": "user", "content": message})

        return self.llm.chat(self.messages)


